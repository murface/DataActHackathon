rm(list=ls())
options(stringsAsFactors = FALSE, scipen = 4, digits =8)
library(jsonlite)
library(dplyr)
library(tidyr)
library(data.table)
library(curl)
setwd("C:/Users/578180/Documents/Data Act Hackathon")
########################################################

award_url <- "https://spending-api.us/api/v1/awards/?limit=200"
pages <- list()
award_api <- fromJSON(award_url, flatten=TRUE)
award_api$page_metadata$has_next_page=TRUE
i<-1

while(award_api$page_metadata$has_next_page==TRUE){
  award_api <- fromJSON(paste0(award_url, "&page=", i), flatten=TRUE)
  message("Retrieving page ", i)
  pages[[i]] <- award_api$results
  i<-i+1
}


awards_data <- bind_rows(pages)
# awards<-toJSON(awards_data, pretty=TRUE)
# write(awards,"awards.json")

award_types<-unique(awards_data$type_description)
agencies<-unique(awards_data$awarding_agency.toptier_agency.abbreviation)

# Agency subets
sec_data<-awards_data[awards_data$awarding_agency.toptier_agency.name %in% c("Securities and Exchange Commission"),]
president_data<-awards_data[awards_data$awarding_agency.toptier_agency.name %in% c("Executive Office of the President"),]
epa_data<-awards_data[awards_data$awarding_agency.toptier_agency.name %in% c("Environmental Protection Agency"),]
sba_data<-awards_data[awards_data$awarding_agency.toptier_agency.name %in% c("Small Business Administration"),]
cfpb_data<-awards_data[awards_data$awarding_agency.toptier_agency.name %in% c("Consumer Financial Protection Bureau"),]

unique(sba_data$recipient.location.state_name)
table(sba_data$recipient.location.state_name)

unique(epa_data$recipient.location.state_name)
table(epa_data$recipient.location.state_name)

# Contracts
contract_data<-awards_data[awards_data$type_description %in% c("Purchase Order","Delivery Order","Definitive Contract"),]
contract<-contract_data[with(contract_data,order(piid,date_signed,awarding_agency.toptier_agency.name,total_obligation)),]

# BPA Calls
bpa<-awards_data[awards_data$type_description %in% c("BPA Call"),]
bpa_data<-tapply(as.numeric(bpa$total_obligation), 
                 bpa$awarding_agency.toptier_agency.name, 
                 sum)

###############################################################################################

trans_url <- "https://spending-api.us/api/v1/transactions/"
pages <- list()
trans_api <- fromJSON(trans_url, flatten=TRUE)
trans_api$page_metadata$has_next_page=TRUE
i<-1

while(trans_api$page_metadata$has_next_page==TRUE){
  trans_api <- fromJSON(paste0(trans_url, "&page=", i), flatten=TRUE)
  message("Retrieving page ", i)
  pages[[i]] <- trans_api$results
  i<-i+1
}

trans_data <- bind_rows(pages)

# write.csv(awards_data,"awards.csv")

#####################################################################################

dat<-fromJSON("flare.json")


contract<-awards_data[with(awards_data,order(awarding_agency.toptier_agency.name,recipient.recipient_name,total_obligation)),]
contract<-contract[as.numeric(contract$total_obligation) > 0,] 
contract<-contract[!is.na(contract$recipient.recipient_name),]
contract<-contract[!is.na(contract$awarding_agency.toptier_agency.name),]
contract<-contract[!is.na(contract$funding_agency.toptier_agency.name),]

con<-toJSON(contract,pretty = TRUE)
write(con,"contract.json")

nrow(contract[contract$awarding_agency.toptier_agency.name==contract$funding_agency.toptier_agency.name,])



