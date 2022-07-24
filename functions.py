import datetime
import pandas as pd
import re


def read_file():
    df = pd.read_excel("Usuarios-WiFi.xlsx")  # read the excel file
    df = df.dropna()  # remove rows with NaN
    return df  # return df


def search_username(username):
    df = read_file()
    df = df[df['Usuario'] == username]  # filter the dataframe by the user
    return df


def list_session_id():
    username = input("Enter username: ")
    print("Prosessing...\n")
    df_username = search_username(username)
    if df_username.empty:
        print("\nThe username %s does not exist." % username)
        return
    else:
        df_user_session = df_username.loc[:,["Usuario", "ID Conexion unico"]] # create a new dataframe with the ID, the user and the start date
        df_user_session.reset_index(inplace=True, drop=True) # reset the index
        print("\n", df_user_session) # print the dataframe
        df_user_session.to_excel("%s_session_id.xlsx" % username, index=False) # save the dataframe to a excel file
        return df_user_session


def list_login_time():
    username = input("Enter username: ")
    print("Prosessing...\n")
    df = search_username(username)
    if df.empty:
        print("\nThe user %s does not exist." % username)
        return
    else:
        regex = re.compile(r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])')  # create a regex to find the time
        print("\nSet a date range following the format: YYYY-MM-DD")
        start_date = input("Enter the start date: ")
        end_date = input("Enter the end date: ")
      
        if regex.fullmatch(start_date) and regex.fullmatch(end_date):
            df_loc = df.loc[:,["Usuario", "Inicio de Conexion"]]
            df_loc['dates'] = df_loc['Inicio de Conexion'].dt.normalize()
            df_date_colum = df_loc.loc[:,["Usuario", "dates"]]
            df_date_colum.sort_values(by=['dates'])
            df_date_range = df_date_colum['dates'].between(start_date, end_date)
            True_Count = df_date_range[df_date_range == True].count()
            print("\nThe user %s has %s sessions between %s and %s" % (username, True_Count, start_date, end_date))
            return True_Count
        else:
            print("\nThe date is not in the correct format.")
            return
        

def total_time_session():
    username = input("Enter username: ")
    print("Prosessing...\n")
    df_username = search_username(username)
    if df_username.empty:
        print("\nThe user %s does not exist." % username)
        return
    else:
        df_loc = df_username.loc[:,["Usuario", "Session Time"]]  # create a new dataframe with the ID, the user and the start date
        df_total_time = df_loc['Session Time'].sum()
        total_time_session = str(datetime.timedelta(seconds=df_total_time))
        print("\nTotal session time of the user %s is:" % username, total_time_session)
        return total_time_session


def list_user_macs():
    username = input("Enter username: ")
    print("Prosessing...\n")
    df_username = search_username(username)
    if df_username.empty:
        print("\nThe user %s does not exist." % username)
        return
    else:
        df_loc = df_username.loc[:,["Usuario", "MAC Cliente"]]
        df_mac_user = df_loc.groupby(['Usuario', 'MAC Cliente']).size().reset_index(name='Number of times used')
        mac_user_serted = df_mac_user.sort_values(by=['Number of times used'], ascending=False)
        mac_user_serted.reset_index(inplace=True, drop=True) # reset the index
        print("\n", mac_user_serted)
        mac_user_serted.to_csv("%s_macs_user.csv" % username, index=False)
        print("\n", "The file %s_macs_user.csv has been created to see more details." % username)
        return mac_user_serted


def user_conected_ap():
    regex_mac_ap = re.compile(r'(?:[\da-fA-F]{2}[-]){5}[\da-fA-F]{2}:UM')  # create a regex to find the MAC
    regex_date = re.compile(r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])')

    mac_ap = input("Enter MAC AP Address following the format XX-XX-XX-XX-XX-XX:UM: ")
    print("Prosessing...\n")

    if regex_mac_ap.fullmatch(mac_ap):
        df_mac_ap = read_file()
        df_mac_ap_validate = df_mac_ap[df_mac_ap['MAC AP'] == mac_ap]  # filter the dataframe by the MAC

        if df_mac_ap_validate.empty:
            print("\nThe MAC AP %s does not exist." % mac_ap)
            return
        else:
            opt = input("\nDo you want a specific date or a range of dates?\n1. Specific date\n2. Range of dates\n")
            if opt == "1":
                print("\nSet a date following the format: YYYY-MM-DD")
                date = input("Enter the date: ")
                if regex_date.fullmatch(date):
                    df_date = df_mac_ap_validate.loc[:,["MAC AP", "Usuario", "MAC Cliente", "Inicio de Conexion"]]
                    df_date['dates'] = df_date['Inicio de Conexion'].dt.normalize()
                    df_date_colum = df_date.loc[:,["MAC AP", "Usuario", "MAC Cliente", "dates"]]
                    df_date_colum.sort_values(by=['dates'])
                    df_date_colum.query('dates == @date', inplace=True)
                    df_date_colum.reset_index(inplace=True, drop=True)
                    print("\n", df_date_colum)
                    df_date_colum.to_csv("%s_conection_in_%s.csv" % (mac_ap, date), index=False)
                    print("\n", "The file %s_conection_in_%s.csv has been created to see more details." % (mac_ap, date))
                    return df_date_colum
                else:
                    print("\nThe date is not in the correct format.")
                    return
            elif opt == "2":
                print("\nSet a date range following the format: YYYY-MM-DD")
                start_date = input("Enter the start date: ")
                end_date = input("Enter the end date: ")
                if regex_date.fullmatch(start_date) and regex_date.fullmatch(end_date):
                    df_date = df_mac_ap_validate.loc[:,["MAC AP", "Usuario", "MAC Cliente", "Inicio de Conexion"]]
                    df_date['dates'] = df_date['Inicio de Conexion'].dt.normalize()
                    df_date_colum = df_date.loc[:,["MAC AP", "Usuario", "MAC Cliente", "dates"]]
                    df_date_colum.sort_values(by=['dates'])
                    if df_date_colum['dates'].between(start_date, end_date).count() == 0:
                        print("\nThere are no sessions in the date range %s to %s." % (start_date, end_date))
                        return
                    else:
                        df_date_range = df_date_colum['dates'].between(start_date, end_date)
                        df_date_colum = df_date_colum[df_date_range]
                        df_date_colum.reset_index(inplace=True, drop=True)
                        print("\n", df_date_colum)
                        df_date_colum.to_csv("%s_conection_in_%s_to_%s.csv" % (mac_ap, start_date, end_date), index=False)
                        print("\n", "The file %s_conection_in_%s_to_%s.csv has been created to see more details." % (mac_ap, start_date, end_date))
                        return df_date_colum
                else:
                    print("\nThe date is not in the correct format.")
                    return


def user_traffic():
    username = input("Enter username: ")
    print("Prosessing...\n")
    df_username = search_username(username)
    if df_username.empty:
        print("\nThe user %s does not exist." % username)
        return
    else:
        df_loc = df_username.loc[:,["Usuario", "Input Octects", "Output Octects"]]  # create a new dataframe with the ID, the user and the start date
        input_traffic = df_loc['Input Octects'].sum()
        input_traffic_mb = input_traffic / 1024**2 # convert to MB
        output_traffic = df_loc['Output Octects'].sum()
        output_traffic_mb = (output_traffic / 1024**2) # convert to MB
        print("\n", "Download: %.2f MB" % input_traffic_mb)
        print("\n", "Upload: %.2f MB" % output_traffic_mb)
        df_traffic = pd.DataFrame({"Usuario": [username], "Download MB": [input_traffic_mb], "Upload MB": [output_traffic_mb]})
        df_traffic.to_csv("%s_traffic.csv" % username, index=False)
        print("\n", "The file %s_traffic.csv has been created to see more details." % username)
        return df_traffic


def list_ap_byTraffic():
    print("Prosessing...\n")
    input_traffic_list = []
    output_traffic_list = []
    df = read_file()
    df_loc = df.loc[:,["MAC AP", "Input Octects", "Output Octects"]]
    df_agruped = df_loc.groupby(['MAC AP']).agg({'Input Octects': 'sum', 'Output Octects': 'sum'}).reset_index()

    for i in range(len(df_agruped)):
        input_traffic = df_agruped['Input Octects'][i]
        input_traffic_mb = input_traffic / 1024**2
        input_traffic_list.append(float("{:.2f}".format(input_traffic_mb)))
        output_traffic = df_agruped['Output Octects'][i]
        output_traffic_mb = (output_traffic / 1024**2)
        output_traffic_list.append(float("{:.2f}".format(output_traffic_mb)))

    df_traffic = pd.DataFrame({"MAC AP": df_agruped['MAC AP'], "Input data in MB": input_traffic_list, "Output data in MB": output_traffic_list})
    opt = (input("\nOrder data by input or by output? (input/output): ")).lower()
    if opt == "input":
        df_traffic = df_traffic.sort_values(by=['Input data in MB'], ascending=False)
        df_traffic.to_csv("ap_traffic_sorted_byInput.csv", index=False)
        print("\n", "The file ap_traffic_sorted_byInput.csv has been created to see more details.")
    elif opt == "output":
        df_traffic = df_traffic.sort_values(by=['Output data in MB'], ascending=False)
        df_traffic.to_csv("ap_traffic_sorted_byOutput.csv", index=False)
    else:
        print("\n", "The option is not valid.")
        return
    return df_traffic


    


    
    
            
    
    


    




        


  


    





    


        

        
