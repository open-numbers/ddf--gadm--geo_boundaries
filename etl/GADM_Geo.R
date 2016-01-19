#declare packages
library(sp)
library(splitstackshape)
library(qdap)
library(gdata)
#set working directory
setwd("N:/Active Projects/DropBox/GapMinder/GADM Files")
#list all files
files<-data.frame(list.files(patter='.rds'))
colnames(files)<-'Names'
files$Names<-as.character(files$Names)
files$Country<-substr(files$Names,1,3)
files$Layer<-as.numeric(substr(files$Names,8,8))
#create template file
finaldata<-NULL
template<-data.frame(country=NA, entity=NA,	types=NA,	geo_layer_0=NA,	geo_layer_1=NA,	geo_layer_2=NA,	geo_layer_3=NA,	geo_layer_4=NA,	geo_layer_5=NA,	geo_layer_6=NA,	ParentName=NA,	name=NA,	short_name=NA,	link=NA,	Type=NA,	GADM_ID=NA,	NAME_ENGLISH=NA,	NAME_ISO=NA,	NAME_FAO=NA,	NAME_LOCAL=NA,	ISO2=NA,	FIPS=NA,	ISON=NA,	Alias1=NA,	Alias2=NA,	Alias3_NumericType=NA,	Alias3_NumericID=NA,	Numeric_Alias=NA,	LocalType=NA, Alias4=NA, Alias5=NA, Types1=NA, Types2=NA)
for (i in 1:nrow(files))
{
    layer<-readRDS(files$Names[i])
    data<-layer@data
    temp1<-template
    temp1$count<-nrow(data)
    temp1<-expandRows(temp1,"count")
    
    temp1$types<-"entity,geo"
    if (files$Layer[i]==0){
      temp1$name<-data$NAME_ISO
      temp1$entity<-paste0(data$ISO,"_","Country")
      temp1$NAME_ENGLISH<-data$NAME_ENGLISH
      temp1$country<-data$NAME_ENGLISH
      temp1$NAME_LOCAL<-data$NAME_LOCAL
      temp1$LocalType<-"Country"
      temp1$Type<-"Country"
    }else{
      eval(parse(text=paste0("temp1$name<-data$NAME_",files$Layer[i])))
      temp1$entity<-paste0(data$ISO,"_","SubCountry",files$Layer[i])
      eval(parse(text=paste0("temp1$NAME_ENGLISH<-data$NAME_",files$Layer[i])))
      temp1$country<-data$NAME_0
      str<-paste0("VARNAME_",files$Layer[i])
      if(str %in% colnames(data))
      {
        eval(parse(text=paste0("temp1$NAME_LOCAL<-data$VARNAME_",files$Layer[i])))
      }else{
        temp1$NAME_LOCAL<-temp1$name
      }
      eval(parse(text=paste0("temp1$LocalType<-data$TYPE_",files$Layer[i])))
      eval(parse(text=paste0("temp1$Type<-data$ENGTYPE_",files$Layer[i])))
    }
    for (layerc in 0:5)
    {
      if (layerc==files$Layer[i])
      {
        eval(parse(text=paste0("temp1$geo_layer_",layerc,"<-'True'")))
      }else if (layerc!=files$Layer[i])
      {
      eval(parse(text=paste0("temp1$geo_layer_",layerc,"<-'False'")))
      }
    }
    if (files$Layer[i]>0)
    {
      eval(parse(text=paste0("temp1$ParentName<-data$NAME_",files$Layer[i]-1)))
    }
    
    temp1$short_name<-substr(temp1$name,1,3)
    temp1$link<-"gadm.org"
    
    eval(parse(text=paste0("temp1$GADM_ID<-data$ID_",files$Layer[i])))
    
    
    if (files$Layer[i]==0){
      temp1$Alias1<-paste0("L0_",data$ID_0)
      temp1$Alias2<-paste0("L0_",data$ISO)
      temp1$Alias3_NumericType<-"100000"
      temp1$Alias3_NumericID<-data$ID_0
      temp1$Alias5<-paste0(data$ISO,"_",substr(temp1$LocalType,1,3))
    }else if (files$Layer[i]==1){
      temp1$Alias1<-paste0("L0_",data$ID_0,"_L1_",data$ID_1)
      temp1$Alias2<-paste0("L0_",data$ISO,"_L1_",substr(data$NAME_1,1,3))
      temp1$Alias3_NumericType<-"110000"
      temp1$Alias3_NumericID<-paste0(data$ID_0,"_",data$ID_1)
      temp1$Alias5<-paste0(data$ISO,"_",substr(temp1$LocalType,1,3),"_",substr(data$NAME_1,1,3))
    }else if (files$Layer[i]==2){
      temp1$Alias1<-paste0("L0_",data$ID_0,"_L1_",data$ID_1,"_L2_",data$ID_2)
      temp1$Alias2<-paste0("L0_",data$ISO,"_L1_",substr(data$NAME_1,1,3),"_L2_",substr(data$NAME_2,1,3))
      temp1$Alias3_NumericType<-"111000"
      temp1$Alias3_NumericID<-paste0(data$ID_0,"_",data$ID_1,"_",data$ID_2)
      temp1$Alias5<-paste0(data$ISO,"_",substr(temp1$LocalType,1,3),"_",substr(data$NAME_1,1,3),"_",substr(data$NAME_2,1,3))
    }else if (files$Layer[i]==3){
      temp1$Alias1<-paste0("L0_",data$ID_0,"_L1_",data$ID_1,"_L2_",data$ID_2,"_L3_",data$ID_3)
      temp1$Alias2<-paste0("L0_",data$ISO,"_L1_",substr(data$NAME_1,1,3),"_L2_",substr(data$NAME_2,1,3),"_L3_",substr(data$NAME_3,1,3))
      temp1$Alias3_NumericType<-"111100"
      temp1$Alias3_NumericID<-paste0(data$ID_0,"_",data$ID_1,"_",data$ID_2,"_",data$ID_3)
      temp1$Alias5<-paste0(data$ISO,"_",substr(temp1$LocalType,1,3),"_",substr(data$NAME_1,1,3),"_",substr(data$NAME_2,1,3),"_",substr(data$NAME_3,1,3))
    }else if (files$Layer[i]==4){
      temp1$Alias1<-paste0("L0_",data$ID_0,"_L1_",data$ID_1,"_L2_",data$ID_2,"_L3_",data$ID_3,"_L4_",data$ID_4)
      temp1$Alias2<-paste0("L0_",data$ISO,"_L1_",substr(data$NAME_1,1,3),"_L2_",substr(data$NAME_2,1,3),"_L3_",substr(data$NAME_3,1,3),"_L4_",substr(data$NAME_4,1,3))
      temp1$Alias3_NumericType<-"111110"
      temp1$Alias3_NumericID<-paste0(data$ID_0,"_",data$ID_1,"_",data$ID_2,"_",data$ID_3,"_",data$ID_4)
      temp1$Alias5<-paste0(data$ISO,"_",substr(temp1$LocalType,1,3),"_",substr(data$NAME_1,1,3),"_",substr(data$NAME_2,1,3),"_",substr(data$NAME_3,1,3),"_",substr(data$NAME_4,1,3))
    }else if (files$Layer[i]==5){
      temp1$Alias1<-paste0("L0_",data$ID_0,"_L1_",data$ID_1,"_L2_",data$ID_2,"_L3_",data$ID_3,"_L4_",data$ID_4,"_L5_",data$ID_5)
      temp1$Alias2<-paste0("L0_",data$ISO,"_L1_",substr(data$NAME_1,1,3),"_L2_",substr(data$NAME_2,1,3),"_L3_",substr(data$NAME_3,1,3),"_L4_",substr(data$NAME_4,1,3),"_L5_",substr(data$NAME_5,1,3))
      temp1$Alias3_NumericType<-"111111"
      temp1$Alias3_NumericID<-paste0(data$ID_0,"_",data$ID_1,"_",data$ID_2,"_",data$ID_3,"_",data$ID_4,"_",data$ID_5)
      temp1$Alias5<-paste0(data$ISO,"_",substr(temp1$LocalType,1,3),"_",substr(data$NAME_1,1,3),"_",substr(data$NAME_2,1,3),"_",substr(data$NAME_3,1,3),"_",substr(data$NAME_4,1,3),"_",substr(data$NAME_5,1,3))
    }
    temp1$Alias3<-paste0(temp1$Alias3_NumericType,"_",temp1$Alias3_NumericID)
    if (files$Layer[i]==0){
      temp1$Alias4<-paste0(data$ISO,"_",substr(temp1$LocalType,1,3))
    }else{
      temp1$Alias4<-paste0(data$ISO,"_",substr(temp1$LocalType,1,3),"_",temp1$name)
    }
    temp1$Types1<-trim(multigsub(c("|","(",")","/"," "),c("_","_","","_","_"),tolower(paste0(data$ISO,"_",substr(temp1$Type,1,3)))))
    temp1$Types2<-trim(multigsub(c("|","(",")","/",","," "),c("_","_","","_","_","_"),tolower(paste0(data$ISO,"_",temp1$Type))))
    finaldata<-rbind(finaldata,temp1)
}
write.csv(finaldata,"Geo.csv")

