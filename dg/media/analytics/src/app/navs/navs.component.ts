
import { Component, OnInit, AfterViewInit, AfterViewChecked } from '@angular/core';
import { environment } from '../../environments/environment.loop';
import { GraphsService } from './navs.service';
import { SharedService } from '../shared.service';
import { global_filter } from '../app.component'

@Component({
  selector: 'app-navs',
  templateUrl: './navs.component.html',
  styleUrls: ['./navs.component.css']
})

export class NavsComponent implements OnInit,
  AfterViewChecked {
  //used for collapse button
  public isCollapsed: boolean = false;
  public showOverall: boolean = true;
  public showFilters: boolean = true;
  navClicked: boolean = false;

  //read config files from environment created for each app
  navsConfig = environment.navsConfig;
  chartsConfig = environment.chartsConfig;

  //initialize modules as false and toggle based on user configuration
  overall: false;
  recent: false;

  //keep track of nav switches and respective subnavs
  toggleNav = {};
  //dict with key as end nav and its corresponding containers
  containers = {};
  //dict with key and its corresponding filter graphs to show drop down for graphs
  filterGraphs = {};
  //list of charts in DOM
  charts = [];
  containerCharts = [];
  //Display drop down type graphs
  // showDropDownGraphs: boolean = false;
  filters = { 'params': {} };
  constructor(private graphService: GraphsService, private _sharedService: SharedService) {
    this._sharedService.argsList$.subscribe(filters => {
      this.filters = filters;
      this.getGraphsData(filters);
    });
    /*setInterval(() => {
      this.charts.forEach(chart => {
        chart.nativeChart.reflow();
      });
    }, 0);*/
  }

  ngOnInit(): void {
    Object.keys(this.chartsConfig).forEach(chart => {
      this.charts.push({
        name: chart,
        options: this.chartsConfig[chart],
        // nativeChart will be assigned with saveInstance
        nativeChart: null
      });
    })
    this.renderNavs();
    //this.renderCharts();
  }

  // ngAfterViewInit(): void {
  //   this.getGraphsData(this.filters);
  // }

  ngAfterViewChecked() {
    if (this.navClicked) {
      this.navClicked = false;
      Object.assign(this.filters.params, global_filter);
      this.getGraphsData(this.filters);
    }

  }

  // renderCharts(): void {
  //   Object.keys(this.chartsConfig).forEach(chart => {
  //     this.charts.push({
  //       name: chart,
  //       options: this.chartsConfig[chart],
  //       // nativeChart will be assigned with saveInstance
  //       nativeChart: null
  //     });
  //   })
  // }
  //render navs and subnavs and create respective containers based on selected nav
  renderNavs(): void {
    Object.keys(this.navsConfig.navs).forEach(nav => {
      let tempDict = {};
      tempDict['status'] = false;
      //check if subNavs exists and create respective container with default view flag as false
      if (this.navsConfig.navs[nav].subNavs != undefined) {
        tempDict['subNavs'] = this.getDictKeys(this.navsConfig.navs[nav].subNavs);
        Object.keys(this.navsConfig.navs[nav].subNavs).forEach(subNav => {
          let container = this.navsConfig.navs[nav].subNavs[subNav];
          if (this.navsConfig.navs[nav].subNavs[subNav].containers != undefined) {
            this.setContainer(subNav, container);
          }
          else if (this.navsConfig.navs[nav].subNavs[subNav].DropDownGraph != undefined) {
            this.setFilterContainer(subNav, container);
          }
        });
      }
      else if (this.navsConfig.navs[nav].containers != undefined) {
        let container = this.navsConfig.navs[nav];
        this.setContainer(nav, container);
      }
      else if (this.navsConfig.navs[nav].DropDownGraph != undefined) {
        let container = this.navsConfig.navs[nav];
        this.setFilterContainer(nav, container);
      }
      this.toggleNav[nav] = tempDict;

      //check for active link on nav bar and set status as true
      if (this.navsConfig.navs[nav].hasOwnProperty('active')) {
        this.toggleNav[nav].status = true;
        this.showContent(nav);
      }
    });
  }

  addChartsToDict(containers) {
    let charts = [];
    Object.keys(containers).forEach(container => {
      Object.keys(containers[container]).forEach(tab => {
        if (containers[container][tab].hasOwnProperty('addDivs')) {
          containers[container][tab]['addDivs'].forEach(chart => {
            charts.push({ name: chart, chart: this.chartsConfig[chart] });
          });
        }
      });
    });
    return charts;
  }

  //set container view based on clicked nav link
  setContainer(nav, container): void {
    this.containers[nav] = container;
    this.containers[nav]['charts'] = this.addChartsToDict(container.containers);
    this.containers[nav]['displayContent'] = false;
  }

  //set container for navs with interdependent filter and graph
  setFilterContainer(nav, container): void {
    this.filterGraphs[nav] = container;
    this.filterGraphs[nav]['charts'] = this.addChartsToDict(container.DropDownGraph);
    this.filterGraphs[nav]['displayContent'] = false;
  }

  //access underlying chart
  saveInstance(chartInstance, chart) {
    chart.nativeChart = chartInstance;
  }

  //get data for graphs from service
  getGraphsData(filters): void {
    this.containerCharts.forEach(chart => {
      if (chart.nativeChart && (chart.nativeChart.series.length == 0)) {
        chart.nativeChart.showLoading();
        filters.params['chartType'] = chart.chart.type;
        filters.params['chartName'] = chart.name;
        this.graphService.getData(filters).subscribe(dataList => {
          if (dataList['chartType'] != undefined && dataList['chartType'] === 'StockChart') {
            this.parseDataForStockChart(chart, dataList.data);
          }
          else {
            Object.keys(dataList).forEach(key => {
              //Find already displayed chart to enter data
              if (key === chart.name) {
                chart.nativeChart.hideLoading();
                this.clearSeriesFromGraph(chart);
                dataList[key]['outerData']['series'].forEach(entry => {
                  chart.nativeChart.addSeries(entry);
                  chart.chart.series.push(entry);
                });
                if (chart.chart.chart.drillDown) {
                  dataList[key]['innerData'].forEach(drilldownEntry => {
                    chart.chart.drilldown.series.push(drilldownEntry);
                  });
                }
              }
              else {
                this.clearSeriesFromGraph(chart);
                chart.nativeChart.showLoading(dataList['error']);
              }
            });
          }
        });
      }
    });
  }

  private parseDataForStockChart(chart, data): void {
    this.clearSeriesFromGraph(chart);
    Object.keys(data).forEach(series => {
      chart.nativeChart.hideLoading();
      chart.nativeChart.addSeries(data[series]);
      chart.chart.series[series] = data[series];
    });
  }

  //Empty exting data and then fill in updated data
  private clearSeriesFromGraph(chart): void {
    if (chart.nativeChart.series.length > 0) {
      for (var i = chart.nativeChart.series.length - 1; i >= 0; i--) {
        chart.nativeChart.series[i].remove();
      }
    }
  }

  //function to return list of keys from a dictionary
  getDictKeys(dict) {
    return Object.keys(dict);
  }

  ifDictionary(obj): boolean {
    if (typeof obj !== 'boolean')
      return true;
    else return false;
  }

  //reset values in a dict, used for navigation and setting containers
  private resetDict(dict, flag, value): void {
    Object.keys(dict).forEach(key => {
      dict[key][flag] = value;
    });
  }

  //set status as true for clicked nav item and rest as false
  setNav(selectedItem: string): void {
    this.resetDict(this.toggleNav, 'status', false);
    this.toggleNav[selectedItem].status = true;
    //set show content for navs with subNavs
    if ((this.toggleNav[selectedItem].hasOwnProperty('subNavs'))) {
      this.toggleNav[selectedItem].subNavs.forEach(subNav => {
        if (this.navsConfig.navs[selectedItem].subNavs[subNav].hasOwnProperty('active')) {
          this.showContent(subNav);
        }
      });
    }
    else {
      this.showContent(selectedItem);
    }
  }

  //render charts to container
  private renderContainerCharts(container): void {
    container.displayContent = true;
    /*    container.charts.forEach(chart => {
          this.charts.push({
            options: chart,
            // nativeChart will be assigned with saveInstance
            nativeChart: null
          });
        });*/
    container.charts.forEach(containerChart => {
      this.charts.forEach(chart => {
        if (chart.name === containerChart.name) {
          this.containerCharts.push(containerChart);
        }
      });
    });
  }

  //display respective containers based on clicked nav
  showContent(selectedNav: string): void {
    this.navClicked = true;
    if (selectedNav == 'Home') {
      this.showOverall = true;
      this.showFilters = false;
    } else {
      this.showOverall = false;
      this.showFilters = true;
    }
    this.resetDict(this.containers, 'displayContent', false);
    this.resetDict(this.filterGraphs, 'displayContent', false);
    this.containerCharts = [];
    if (this.containers[selectedNav] != undefined) {
      this.renderContainerCharts(this.containers[selectedNav]);
    }
    else if (this.filterGraphs[selectedNav] != undefined) {
      this.renderContainerCharts(this.filterGraphs[selectedNav]);
    }
  }
}
