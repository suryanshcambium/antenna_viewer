import pandas as pd

def data_clean(uploaded_files):
 # pure code ko ek function me (def) me convert karo aur multiple files jo lie hain unko ek consolidated csv me convert kardo
  # add dfp which are half the rows of the normal consolidated dataframe and returns it.

  def rename_columns_partially(df, old_part, new_part):
    # df = df.rename(column=new_column_names)
    new_column_names = {col: col.replace(old_part, new_part) for col in df.columns}
    df = df.rename(columns=new_column_names)
    return df


  def data_clean(df, file_name, i):
    DF_FILE = df[10:]
    DF_FILE.columns = df.iloc[9]
    DF_FILE = DF_FILE.reset_index(drop=True)
    if (i == 0):
      DF_FILE = DF_FILE.drop(['Frequency','Port ID','Port Name','Step Axis'], axis = 1)
    else:
      DF_FILE = DF_FILE.drop(['Frequency','Port ID','Port Name', 'Step Axis', 'Pol. Axis', 'Scan Axis'], axis = 1)
    DF_FILE = DF_FILE.astype('float64')
    colu = DF_FILE.columns[2]
    file_name = file_name[:-4]
    # filename = filename[:-4]
    DF_FILE = rename_columns_partially(DF_FILE, colu[0:10], file_name)
    return DF_FILE


  def import_multiple_csv_files(uploaded_files):

    dataframes = []

    for i in range(len(uploaded_files)):
      # file_path = input(f"Enter the file path for file {i+1}: ")
      df = pd.read_csv(uploaded_files[i])
      df = data_clean(df, uploaded_files[i].name, i)
      dataframes.append(df)

    return dataframes

  # number_of_files = int(input("Enter the number of files: "))
  data = import_multiple_csv_files(uploaded_files)

  df = pd.DataFrame(data[0])
  i=1
  for i in range(1, len(uploaded_files)):
    df = pd.concat([df, data[i]], axis=1)

  return df