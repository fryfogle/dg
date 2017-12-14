import { Component, OnInit } from '@angular/core';
import { GlobalFilter } from './global-filter.model'
import { GlobalFilterService } from './global-filter.service'
import { SharedService } from '../shared.service';
import { global_filter } from '../app.component';
import { GlobalFilterSharedService } from '../global-filter/global-filter-shared.service';
import { config } from '../../config';

@Component({
  selector: 'app-global-filter',
  templateUrl: './global-filter.component.html',
  styleUrls: ['./global-filter.component.css']
})
export class GlobalFilterComponent implements OnInit {
  Dropdownitems: GlobalFilter[] = [];
  country: string = '';
  globalFiltersConfig = config.globalFiltersConfig;
  constructor(private _globalfilter: GlobalFilterService, private _sharedService: SharedService,
    private _globalfiltersharedService: GlobalFilterSharedService) { }

  ngOnInit() {
    // Listening global filter
    this._globalfilter.getData().subscribe(data => {
      data.forEach(element => {
        Object.keys(this.globalFiltersConfig).forEach(obj => {
          if (this.globalFiltersConfig[obj].name == element.name) {
            this.globalFiltersConfig[obj].data = element.data;
            this.globalFiltersConfig[obj].default = element.data[0].value;
          }
        });
      });
      // Check iframe working or not

      if ('country_id' in global_filter) {
        Object.keys(this.globalFiltersConfig).forEach(key => {
          let globalFilterConfigObj = this.globalFiltersConfig[key];
          if(globalFilterConfigObj.name == 'Country') {
            if('state_id' in global_filter) {
              for (let data of globalFilterConfigObj.data) {
                for (let s_data of data.dropDownData) {
                  if(s_data.id == global_filter['state_id']) {
                    this.globalFiltersConfig[key].default = s_data.value
                  }
                }
              }
            } else {
              for (let data of globalFilterConfigObj.data) {
                if(data.id == global_filter['country_id']) {
                  this.globalFiltersConfig[key].default = data.value
                }
              }
            }

            // Handling Partner Filter
            if (key == 'filter0') {
              this._globalfilter.getData('get_partners_list/').subscribe(data => {
                console.log(data);
                Object.keys(this.globalFiltersConfig).forEach(obj => {
                  if (this.globalFiltersConfig[obj].name == 'Partner') {
                    this.globalFiltersConfig[obj].data = data;
                    // Handling default value in Partner DropDown
                    if('partner_id' in global_filter) {
                      for (let data of this.globalFiltersConfig[obj].data) {
                        if(data.id == global_filter['partner_id']) {
                          this.globalFiltersConfig[obj].default = data.value
                        }
                      }
                    }
                  }
                });
              })
            }
          }
          
        });
      }
    });
  }

  updateDropdown(item, filterName) {
    console.log(item, filterName);
    Object.keys(this.globalFiltersConfig).forEach(key => {
      let globalFilterConfigObj = this.globalFiltersConfig[key];
      if (key == filterName) {
        globalFilterConfigObj.default = item.value;
      } else if (globalFilterConfigObj.dependent) {
        globalFilterConfigObj.default = globalFilterConfigObj.data[0].value;
      }
    });
    if (!this.globalFiltersConfig[filterName].dependent) {
      for (const prop of Object.keys(global_filter)) {
        delete global_filter[prop];
      }
    }
    global_filter[item.tagName] = item.id;
    // TODO : if Dropdown level more than 2 => handling
    if (item.parentTag) {
      global_filter[item.parentTag] = item.parentId;
    }
    // Handling Partner Dropdown as per the Geography selection
    if (filterName == 'filter0') {
      this._globalfilter.getData('get_partners_list/').subscribe(data => {
        Object.keys(this.globalFiltersConfig).forEach(obj => {
          if (this.globalFiltersConfig[obj].name == 'Partner') {
            this.globalFiltersConfig[obj].data = data;
          }
        });
      })
    }
    this._globalfiltersharedService.publishData();
    // this._sharedService.publishData(global_filter);
  }

  getDictKeys(dict): any {
    return Object.keys(dict);
  }

}
