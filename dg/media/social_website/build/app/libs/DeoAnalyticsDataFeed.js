define(["require","app/libs/DigitalGreenDataFeed","app/libs/DataModel"],function(e){var t=e("app/libs/DigitalGreenDataFeed"),n=e("app/libs/DataModel"),r=t.extend({constructor:function(e){this.base("api/getthedeo/");var t=this._dataModel.addSubModel("analytics",!0)},fetch:function(e){this.base()},_processData:function(e){this.base(e);var t=this._dataModel,n=t.get("analytics");return n.set("analyticsObj",e.analytics),e.analytics},setInputParam:function(e,t,n){var r=this.base(e,t);return r&&!n&&this.clearanalyticsCache(),r},clearanalyticsCache:function(){this._dataModel.get("analytics").clear()},getAnalytics:function(){var e=this._dataModel.get("analytics"),t=e.get("analyticsObj");return t?t:(this.fetch(),!1)}});return r});