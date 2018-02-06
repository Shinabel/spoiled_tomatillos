package edu.northeastern.cs4500;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.support.SpringBootServletInitializer;

@SpringBootApplication
public class Cs4500Spring2018MorganApplication extends SpringBootServletInitializer{
	
	@Override
	protected SpringApplicationBuilder
	configure(SpringApplicationBuilder application) {
	return application.sources(
	Cs4500Spring2018MorganApplication.class);
	}

	public static void main(String[] args) {
		SpringApplication.run(Cs4500Spring2018MorganApplication.class, args);
	}
}