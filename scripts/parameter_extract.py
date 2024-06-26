import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from scipy.signal import find_peaks
#######################################################################################################################################

def parameter_extract(dfp, number_of_files):

    data2 = pd.DataFrame(dfp)
    data2 = data2.astype('float64')


    Gain = data2.max()
    Gain = Gain.drop(index=Gain.index[0:2], axis=0)


    GainIndex = data2.idxmax()
    GainIndex = GainIndex.drop(index=GainIndex.index[0:2], axis=0)


    BeamSquint = data2.loc[GainIndex, ["Scan Axis"]]
    BeamSquint = BeamSquint.squeeze()
    BeamSquint.index = Gain.index


    df2 = pd.DataFrame({
        'GainIndex': GainIndex,
        'Gain': Gain,
        'BeamSquint': BeamSquint
    })





#######################################################################################################################################

    # Create DataFrame
    #df2 = pd.DataFrame(data)

    BW = np.empty((dfp.shape[1]-2))

    def numeric_similarity(num1, num2, max_diff):
        # Convert numbers to floats
        n1 = float(num1)
        n2 = float(num2)

        # Calculate absolute difference
        diff = abs(n1 - n2)

        # Calculate similarity as a percentage of the maximum allowed difference
        if diff > max_diff:
            return 0
        similarity = 100 * (1 - (diff / max_diff))
        return int(similarity)

    # def sa(sa):
    #     for s in sa
    #     return s

    def fuzzy_match_column(value, df2, column, max_diff, index):
        # Convert the column to string
        choices = df2.iloc[:,column].astype(str).tolist()
        scanaxis= df2.iloc[:,index].astype(str).tolist()

        # Perform fuzzy matching using the custom similarity function
        results = [(choice, numeric_similarity(value, choice, max_diff), sa) for choice, sa in zip(choices,scanaxis)]

        # Filter results to include only those with a similarity greater than 0
        filtered_results = [(item, score, id) for item, score, id in results if score > 0]

        return filtered_results

    i=0
    while i < (dfp.shape[1]-2):

        # Value to match
        value_to_match = (df2.iloc[i,1]-3)


        # Maximum allowed difference
        max_diff = 0.5  # You can set this to any desired threshold


        # Perform matching
        matches = fuzzy_match_column(value_to_match, data2, i+2, max_diff, 1)
        third_column = [item[2] for item in matches]

        arr = np.array(third_column)
        arr = arr.astype(float)
        arr= np.abs(arr)
        result = np.sum(arr)
        avg_BW = (result/len(arr))*2

        # avg_scnax = matches[2].mean()

        # Print results
        # print("Matching results:", i)
        # for match in matches:
        #     print(f"Value: {match[0]}, ScanAxis: {match[2]}, Similarity: {match[1]}")
        #   print(f"3db Beam Width of {i} = {(avg_BW)}")
        BW[i] = np.array(avg_BW)
        i+=1
    BW = np.array(BW)



#######################################################################################################################################

    SLL = np.zeros((dfp.shape[1]-2))
    i=2
    while i<dfp.shape[1]:
        column_index = i
        array = dfp.iloc[:, column_index].to_numpy()
        peaks, _ = find_peaks(array)
        peak_values = array[peaks]
        peak_values = -np.sort(-peak_values)
        SLL[i-2] = peak_values[0] - peak_values[1]
        i += 1


#######################################################################################################################################

    df2 = pd.DataFrame({
        # f'GainIndex {name2}': GainIndex,
        'Gain': Gain,
        'BeamSquint': BeamSquint,
        '3db BeamWidth': BW,
        'Side Lobe Level': SLL
    })



    df2.index= Gain.index



#######################################################################################################################################


    import string

    def generate_letter_array(repeat_count):
        letters = string.ascii_lowercase  # generates 'abcdefghijklmnopqrstuvwxyz'
        result = []

        for i in range(repeat_count):
            letter = letters[i % len(letters)]
            result.extend([letter] * int(row_per_file))
        return result

    # Example usage:
    # number_of_files = len(uploaded_files)  # Adjust this value as needed
    row_per_file = (dfp.shape[1]-2)/number_of_files
    array = generate_letter_array(number_of_files)
    array = np.array(array)


#######################################################################################################################################



    df2 = pd.DataFrame({
        # f'GainIndex {name2}': GainIndex,
        'Gain': Gain,
        'BeamSquint': BeamSquint,
        '3db BeamWidth': BW,
        'Side Lobe Level': SLL,
        'FileName' : array
    })


#######################################################################################################################################

    i = 0
    df2_index = []
    while i<df2.shape[0]:
        col_name_new = df2.index[i].split('@')[-1]
        df2_index.insert(i, col_name_new)
        i+=1
    df2_index = np.array(df2_index)
    df2.index = df2_index

#######################################################################################################################################

    return df2