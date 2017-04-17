import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { TopBarDataComponent } from './top-bar-data/top-bar-data.component';
import { TopBarDataService } from './top-bar-data.service';
import { AccordionModule } from '../../node_modules/ngx-bootstrap';
import { KeysPipe } from './keys.pipe';
import { GraphComponent } from './graph/graph.component';
import { NvD3Module } from '../../node_modules/angular2-nvd3';

@NgModule({
  declarations: [
    AppComponent,
    TopBarDataComponent,
    KeysPipe,
    GraphComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AccordionModule.forRoot(),
    NvD3Module,
  ],
  providers: [TopBarDataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
