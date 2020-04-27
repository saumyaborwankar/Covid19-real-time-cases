eatimport urllib.request
import json
##getting country code data
response = urllib.request.urlopen("https://raw.githubusercontent.com/pomber/covid19/master/docs/countries.json")
contents = response.read()
country_data = json.loads(contents)
#contry_code=pd.DataFrame(data)

## getting number of cases data
response2 =urllib.request.urlopen("https://pomber.github.io/covid19/timeseries.json")
contents2=response2.read()
num_cases=json.loads(contents2)
#num_cases=pd.DataFrame(data2)
confirmed=[]
names=[]
count=1
date=[]
#print(len(num_cases['Afghanistan']))

for i in num_cases.keys():
    confirm=0
    for j in num_cases[i]:
        confirm=(j['confirmed'])
        confirmed.append(confirm)
        date.append(j['date'])
        names.append(i)
date=date[0:len(num_cases['Afghanistan'])]
unique=[]
for i in names:
    if i not in unique:
        unique.append(i)        

num_88=len(num_cases['Afghanistan'])
num_185=len(num_cases)
country_name=[]
country_num=[]
country=list(num_cases.keys())
for i in range(len(num_cases)):
    country_name.append(country[i])
    country_num.append(i)
dict_country_num_name={country_num[i]:country_name[i] for i in range(len(country_num))}
confirmed_final=[confirmed[i:i+(num_88)] for i in range(0,(num_88*num_185),num_88)]


t_100=[]
number_100=[]
for i in range(len(confirmed_final)):
    for j in range(len(confirmed_final[0])):
        if confirmed_final[i][j]>100:
            t_100.append(confirmed_final[i].index(confirmed_final[i][j]))
            number_100.append(i)
            break
dict_for_100={number_100[i]:t_100[i] for i in range(len(number_100))}        

q_10k=[]
number_10k=[]
for i in range(len(confirmed_final)):
    for j in range(len(confirmed_final[0])):
        if confirmed_final[i][j]>10000:
            q_10k.append(confirmed_final[i].index(confirmed_final[i][j]))
            number_10k.append(i)
            break
dict_for_10k={number_10k[i]:q_10k[i] for i in range(len(number_10k))}       
diff_bw_100and10k=[]
number_diff=[]
for i in dict_for_10k.keys():
    if i in dict_for_100.keys():
        diff_bw_100and10k.append(dict_for_10k[i]-dict_for_100[i])
        number_diff.append(i)
dict_diff={diff_bw_100and10k[i]:number_diff[i] for i in range(len(number_diff))}

print("The country that went from 100 to 1k cases the fastest is {}".format(dict_country_num_name[dict_diff[min(diff_bw_100and10k)]]) )
print("The number of days it took for {} to get from 100 to 1k is {}".format(dict_country_num_name[dict_diff[min(diff_bw_100and10k)]]),min(diff_bw_100and10k)+1))
print("The country that took the most time to go from 100 to 1k cases {}".format(dict_country_num_name[dict_diff[max(diff_bw_100and10k)]]) )
print("The number of days it took for {} to get from 100 to 1k is {}".format(dict_country_num_name[dict_diff[max(diff_bw_100and10k)]]) ,max(diff_bw_100and10k)+1))


######################## PART 2 #######################
import pandas as pd
pop_info=pd.read_csv('population_Data.csv')
f = open("population_data.csv","r")
lines = f.readlines()
#making a list of total infected people according to country 
total_infected=[confirmed_final[i][-1] for i in range(len(confirmed_final))]
dict_for_percapita={country[i]:total_infected[i] for i in range(len(country))}


#Extracting country names and population from the population_data.csv file
new_country=[]
pop=[]
#info_dict=[]
for i in range(len(lines)):
    info=(lines[i].replace('\n',',')).split(",")
    new_country.append(info[0])
    pop.append(info[-4])

#removing the extra "" in the date
new_country=[s.strip('"') for s in new_country]    
#creating a dictionary for linking countries with their population
info_dict={new_country[i]: pop[i] for i in range(len(pop))}    



#dictionary for the total infected people with respect to their country name
dict_for_total_q5={country_name[i]:confirmed_final[i] for i in range(len(country_name))}
#making a list of countries that have the proper data in the population file and removing the rst
new_pop_for185=[]
new_country=[]
pop=[s.strip('"') for s in pop]
index_not_present=[]
for i in country:
    try:
        new_pop_for185.append(info_dict[i])
        new_country.append(i)
    except:
        index_not_present.append(i)
#creating a new list containing 165  countries which have the proper information about population
new_pop_for185=[s.strip('"') for s in new_pop_for185]
#dictionary for linking proper country name and population information of the 165 coountries
final_info_dict={new_country[i]:new_pop_for185[i] for i in range(len(new_country))}
#function to calculate percapita infection
def CalculatePerCapita(new_date):   
    #calculating the index of date
    date_q5=date.index(new_date)
    confirmed_final_for_q5=[dict_for_total_q5[i] for i in new_country]
    #calculating number of people that got affected on that date
    confirmed_for_q5=[confirmed_final_for_q5[i][date_q5] for i in range(len(confirmed_final_for_q5))]
    #dictionary to link country name and infected people on the specific date
    final_confirmed_dict={new_country[i]:confirmed_for_q5[i] for i in range(len(new_country))}
    #final dictinary for the data
    ekdum={}
    for i in new_country:
    
        try:
            #calculate the ratio of infected people by total population with respect to proper country name
            ekdum['{}'.format(i)]=(float(final_confirmed_dict[i])/float(final_info_dict[i]))*100
        except:
            #there are still some missiong fields in the population data as the population of 2018 is missing for certain countries so this try and except method is used
            continue
    #lists are made to extract key and value pairs for the country name and per capita infection
    list1=list(ekdum.values())
    
    list2=list(ekdum.keys())
    #the country with max ratio is selected for the answer
    yuu=max(ekdum.values())
    final_country=list2[list1.index(yuu)]
    final_value=yuu
    return final_country, final_value

q5,q6=CalculatePerCapita('2020-2-10')
q7,q8=CalculatePerCapita('2020-3-10')
q9,q10=CalculatePerCapita('2020-4-10')

print("The country with the highest per capita infection on Feb 10 2020 is {}".format(q5))
print("The value is {}".format(q6))
print("The country with the highest per capita infection on March 10 2020 is {}".format(q7))
print("The value is {}".format(q8))
print("The country with the highest per capita infection on April 10 2020 is {}".format(q9))
print("The value is {}".format(q10))





















