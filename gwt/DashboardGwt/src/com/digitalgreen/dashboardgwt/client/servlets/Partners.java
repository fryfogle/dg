package com.digitalgreen.dashboardgwt.client.servlets;

import java.util.HashMap;
import java.util.List;

import com.digitalgreen.dashboardgwt.client.common.Form;
import com.digitalgreen.dashboardgwt.client.common.OnlineOfflineCallbacks;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.digitalgreen.dashboardgwt.client.data.LanguagesData;
import com.digitalgreen.dashboardgwt.client.data.PartnersData;
import com.digitalgreen.dashboardgwt.client.templates.LanguagesTemplate;
import com.digitalgreen.dashboardgwt.client.templates.PartnersTemplate;
import com.google.gwt.user.client.Cookies;
import com.google.gwt.user.client.Window;

import com.google.gwt.json.client.JSONParser;


public class Partners extends BaseServlet{
	
	public Partners(){
		super();
	}
	
	public Partners(RequestContext requestContext) {
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
				PartnersData partnerData = new PartnersData(new OnlineOfflineCallbacks(this) {
				public void onlineSuccessCallback(String results) {
					if(results != null) {
						PartnersData partnersData = new PartnersData();
						List partners = partnersData.getListingOnline(results);
						RequestContext requestContext = new RequestContext();
						requestContext.setMessageString("Partner successfully saved");
						requestContext.getArgs().put("listing", partners);
						getServlet().redirectTo(new Partners(requestContext ));						
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
					getServlet().redirectTo(new Partners(requestContext));	
				}
					
				public void offlineSuccessCallback(Object results) {
					if((Boolean)results) {
						PartnersData partnerData = new PartnersData();
						List partners = partnerData.getPartnersListingOffline();
						RequestContext requestContext = new RequestContext();
						requestContext.setMessageString("Partner successfully saved");
						requestContext.getArgs().put("listing", partners);
						getServlet().redirectTo(new Partners(requestContext ));
					} else {
						RequestContext requestContext = new RequestContext();
						requestContext.setMessageString("Invalid data, please try again");
						getServlet().redirectTo(new Partners(requestContext));				
					}		
				}
			}, form, this.requestContext.getQueryString());
				partnerData.apply(partnerData.postPageData());
			}
			else {
				HashMap queryArgs = (HashMap)this.requestContext.getArgs();
				String queryArg = (String)queryArgs.get("action");
				if(queryArg.equals("list")){
					PartnersData partnerData = new PartnersData(new OnlineOfflineCallbacks(this) {
					public void onlineSuccessCallback(String results) {
						if(results != null) {
							PartnersData partnersData = new PartnersData();
							List partners = partnersData.getListingOnline(results);
							RequestContext requestContext = new RequestContext();
							requestContext.getArgs().put("listing", partners);
							getServlet().redirectTo(new Partners(requestContext));						
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
						getServlet().redirectTo(new Partners(requestContext));	
					}
						
					public void offlineSuccessCallback(Object results) {
						if((Boolean)results) {
							PartnersData partnersData = new PartnersData();
							List partners = partnersData.getPartnersListingOffline();
							RequestContext requestContext = new RequestContext();
							requestContext.getArgs().put("listing", partners);
							getServlet().redirectTo(new Partners(requestContext));
						} else {
							RequestContext requestContext = new RequestContext();
							requestContext.setMessageString("Local Database error");
							getServlet().redirectTo(new Partners(requestContext));				
						}
					}
					});
					partnerData.apply(partnerData.getPageData());	
				}
				else{
					this.fillTemplate(new PartnersTemplate(this.requestContext));
				}
			}
		}
	}

}
