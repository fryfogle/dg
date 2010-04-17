package com.digitalgreen.dashboardgwt.client.data.validation;

import java.util.HashMap;

public class StringValidator extends BaseValidator {
	
	private int minValue = Integer.MIN_VALUE;
	private int maxValue = Integer.MAX_VALUE;
	private HashMap choices = null;
	
	public StringValidator(String value) {
		super(value);
	}
	
	public StringValidator(String value, boolean nullable, boolean blank) {
		super(value, nullable, blank);
	}
	
	public StringValidator(String value, boolean nullable, boolean blank, 
			int minValue, int maxValue) {
		super(value, nullable, blank);
		this.minValue = minValue;
		this.maxValue = maxValue;
	}
	
	@Override
	public boolean validate() {
		if(!super.validate()) return false;
		if(!(this.getValue().length() >= this.minValue && 
				this.getValue().length() <= this.maxValue)) 
			return false;
		return true;
	}
	
}