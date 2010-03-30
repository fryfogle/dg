package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;
import com.digitalgreen.dashboardgwt.client.common.RequestContext;
import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.RegionsData;
import com.digitalgreen.dashboardgwt.client.data.VillagesData;
import com.digitalgreen.dashboardgwt.client.templates.RegionsTemplate;
import com.digitalgreen.dashboardgwt.client.templates.VillagesTemplate;

public class Villages extends BaseServlet {
	
	public Villages() {
		super();
	}
	
	public Villages(RequestContext requestContext) {
		super(requestContext);
	}
	@Override
	public void response() {
		super.response();
		
		if (!this.isLoggedIn()) {
			super.redirectTo(new Login());
		} else {
			String method = this.getMethodTypeCtx();
			if(method.equals(RequestContext.METHOD_POST)) {
				Form form = (Form)this.requestContext.getArgs().get("form");
				VillagesData villageData = new VillagesData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							VillagesData villageData = new VillagesData();
							List villages = villageData.getVillagesListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Village successfully saved");
							requestContext.getArgs().put("listing", villages);
							getServlet().redirectTo(new Villages(requestContext));
						} else {
							/*Error in saving the data*/			
						}
					}
					
					public void onlineErrorCallback(int errorCode) {
						RequestContext requestContext = new RequestContext();
						if (errorCode == BaseData.ERROR_RESPONSE)
							requestContext.setMessageString("Unresponsive Server.  Please contact support.");
						else if (errorCode == BaseData.ERROR_SERVER)
							requestContext.setMessageString("Problem in the connection with the server.");
						else
							requestContext.setMessageString("Unknown error.  Please contact support.");
						getServlet().redirectTo(new Villages(requestContext));	
					}
					
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							VillagesData villageData = new VillagesData();
							List villages = villageData.getVillagesListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Village successfully saved");
							requestContext.getArgs().put("listing", villages);
							getServlet().redirectTo(new Villages(requestContext));
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Invalid data, please try again");
							getServlet().redirectTo(new Villages(requestContext));				
						}
						
					}
				}, form, this.requestContext.getQueryString());
				
				villageData.apply(villageData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					VillagesData villageData = new VillagesData(new OnlineOfflineCallbacks(this) {
						public void onlineSuccessCallback(String results) {
							if(results != null) {
								VillagesData villageData = new VillagesData();
								List villages = villageData.getVillagesListingOnline(results);
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", villages);
								getServlet().redirectTo(new Villages(requestContext));						
							} else {
								/*Error in saving the data*/			
							}
						}

						public void onlineErrorCallback(int errorCode) {
							RequestContext requestContext = new RequestContext();
							if (errorCode == BaseData.ERROR_RESPONSE)
								requestContext.setMessageString("Unresponsive Server.  Please contact support.");
							else if (errorCode == BaseData.ERROR_SERVER)
								requestContext.setMessageString("Problem in the connection with the server.");
							else
								requestContext.setMessageString("Unknown error.  Please contact support.");
							getServlet().redirectTo(new Villages(requestContext));	
						}
						
						public void offlineSuccessCallback(Object results) {
							if((Boolean)results) {
								VillagesData villageData = new VillagesData();
								List villages = villageData.getVillagesListingOffline();
								RequestContext requestContext = new RequestContext();
								requestContext.getArgs().put("listing", villages);
								getServlet().redirectTo(new Villages(requestContext));
							} else {
								RequestContext requestContext = new RequestContext();
								requestContext.setMessageString("Local Database error");
								getServlet().redirectTo(new Villages(requestContext));				
							}	
						}
					});
					villageData.apply(villageData.getPageData());
				}
				else {
					this.fillTemplate(new VillagesTemplate(this.requestContext));
				}
			}
		}
	}
}