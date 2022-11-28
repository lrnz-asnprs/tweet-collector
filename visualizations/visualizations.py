from matplotlib import pyplot as plt
from drivers.configs.directories import Directories
import pandas as pd

""" Following script includes methods to recreate plots used in the report for this repository
"""

dir = Directories()
destination = str(dir.POLITIFACT_PLOTS_PATH) + "/" 
destinatio_plots_drivers = str(dir.PLOTS_PATH) + "/drivers/"

PARAMS = {
    "fss":12, #small font-size
    "fsm":14, #medium font-size
    "fsl":16, #large font-size
}



""" 1. Politifact - Claim data
Following section of the script enables a coherent creation of subplots to visualize the 
data characteristic of the politifact fact-checked claims data set.

"""

def get_truth_values_distr(df):
    politifact_claims = df
    distr_of_truth_values = politifact_claims.groupby("truth_value")[['truth_value']].count()
    
    #for ordering
    labels = {
        "barely-true": 2,	
        "false": 1,
        "half-true": 3,
        "mostly-true": 4,
        "pants-fire": 0,	
        "true": 5,
        }
    
    distr_of_truth_values.rename({'truth_value':'count'}, axis=1, inplace=True)
    distr_of_truth_values.reset_index(inplace=True)
    
    distr_of_truth_values['scale'] = distr_of_truth_values.truth_value.apply(lambda x: labels[x])
    distr_of_truth_values.sort_values(by='scale', inplace=True)
    
    truth_values = distr_of_truth_values.set_index('truth_value')
    
    total = truth_values['count'].sum()
    truth_values['pct'] = truth_values['count'].apply(lambda x: x/total)
    
    return truth_values
    

def plot_truth_o_meter(df, save_results=True, include_title=False):
    
    truth_values = get_truth_values_distr(df)
    
    fig, ax = plt.subplots()

    truth_value = truth_values.index.to_list()
    counts = truth_values['count'].to_list()
    bar_labels = truth_values.index

    # Hex colors derived from HEX COLORS CALC --> https://color-hex.org/color-palettes/187
    ax.bar(truth_value, counts, label=bar_labels, color=['#ff0000','#ffa700', '#fff400', '#a3ff00','#2cba00'])

    ax.set_ylabel('Claims', fontsize=PARAMS['fsm'])
    
    if include_title:
        ax.set_title('Truth-O-Meter Distribution', fontsize=PARAMS['fsl'])

    if save_results:
        plt.savefig(destination + "truth-o-meter_distr.pdf", bbox_inches='tight')
        #plt.savefig(destination + "truth-o-meter_distr.png", dpi=600)
    else:
        plt.show()
        

def plot_top_topics(df, save_results=True, include_title=False, tail=10):
    
    politifact_claims = df 
    
    by_topic = politifact_claims.groupby('topic')[['claim']].count()
    
    # df view
    by_topic_view = by_topic.sort_values(by='claim').tail(tail)

    # barplot horizontal
    plt.barh(y=by_topic_view.index, width=by_topic_view.claim)

    plt.yticks(fontsize=PARAMS['fss'])
    plt.xticks(fontsize=PARAMS['fss'])
    plt.xlabel('Claims', fontsize=PARAMS['fsm'])


    #plt.ylabel("Topics", fontsize='16')
    if include_title:
        plt.title("Top 10 Topics in the Politifact Data Set", fontsize=PARAMS['fsl'])
    
    
    if save_results:
        plt.savefig(destination + "topics_pltfct.pdf", bbox_inches='tight')
        #plt.savefig(destination + "topics_pltfct.png", dpi=600)
    else:
        plt.show()
        

def plot_top_origins(df, save_results=True, include_title=False, tail=10):
    
    #Altering the data to get the groupby view of it.
    politifact_claims = df
    by_origin = politifact_claims.groupby("origin")[['claim']].count()
    
    by_origin_view = by_origin.sort_values(by='claim').tail(tail)

    plt.barh(y=by_origin_view.index, width=by_origin_view.claim)

    plt.yticks(fontsize=PARAMS['fss'])
    plt.xticks(fontsize=PARAMS['fss'])
    plt.xlabel("Claims", fontsize=PARAMS['fsm'])

    if include_title:
        plt.title("Top 10 Origins of Claims", fontsize=PARAMS['fsl'])
        
    if save_results:
        plt.savefig( destination + "origin_pltfct.pdf", bbox_inches='tight')
        #plt.savefig( destination + "origin_pltfct.png", dpi=600)
    else:
        plt.show()


def plot_timeframe_cumsum(df, save_results=True, include_title=False):
    
    # Getting the cummulative sum for when fact-checks have happened over time
    politifact_claims = df
    date_cumsum = politifact_claims.groupby('date').count().claim.cumsum()
    
    title = "Cummulative Fact-Checks over Time"
    x_label = "Years"
    y_label = "Cummulative Claims"


    plt.xticks(fontsize=PARAMS['fss'])
    plt.yticks(fontsize=PARAMS["fss"])
    plt.xlabel(x_label, fontsize=PARAMS["fsm"])
    plt.ylabel(y_label, fontsize=PARAMS["fsm"])
    
    if include_title:
        plt.title(title, fontsize=PARAMS['fsl'])
    
    plt.plot(date_cumsum)

    if save_results:
        plt.savefig(destination + "time_pltfct.pdf", bbox_inches='tight')
        #plt.savefig(destination + "time_pltfct.png", dpi=600)
        


    """ 2. Drivers and Methodology
    
    """
    
    
def create_politicians_subsample(pols, sample_size):
    
    #creating the barscores
    pols = pols[['full_name', 'ideology', 'party']]
    pols['bar_score'] = pols['ideology'].apply(lambda x: x-0.5)
    
    pols_sample_rep = pols[pols['bar_score']>0.0].sample(sample_size, random_state=42).sort_values(by='bar_score')
    pols_sample_dem = pols[pols['bar_score']<0.0].sample(sample_size, random_state=42).sort_values(by='bar_score')
    pols_sample = pd.concat([pols_sample_dem, pols_sample_rep])
    
    return pols_sample    

def format_politicians_barscores(pols_sample):
    #creating the negative and positive data sample (neg:democrats, pos:republicans)
    negative_data = pols_sample[pols_sample['bar_score']<0]['bar_score'].to_list() 
    positive_data = pols_sample[pols_sample['bar_score']>=0]['bar_score'].to_list()

    gap_neg = [0]*len(positive_data)
    gap_pos = [0]*len(negative_data)

    for x in gap_neg:
        negative_data.append(x)

    for x in positive_data:
        gap_pos.append(x)
        positive_data = gap_pos
        
    return negative_data, positive_data

def plot_politicians_ideologyscores(df, sample_size, savefig=False):
    
    """Mothership to plot the ideology_scores
    """
    
    pols_sample = create_politicians_subsample(df, sample_size)
        
    x = range(len(pols_sample))
    fig = plt.figure(figsize=(14,4))

    #get the negative, positive data samples / what goes above below the 0.0 (0.5 line)
    negative_data, positive_data = format_politicians_barscores(pols_sample)

    ax = plt.subplot(111)
    ax.bar(x, negative_data, width=0.8, color='b')
    ax.bar(x, positive_data, width=0.8, color='r')

    ax.set_xticks(range(0,len(pols_sample)))

    ax.set_xticklabels(pols_sample['full_name'].to_list(), rotation=80, ha='right', fontsize=PARAMS["fss"])

    ax.set_ylabel("Ideology Score", fontsize=PARAMS["fsm"])
    ax.set_xlabel("U.S. Politicians", fontsize=PARAMS["fsm"])
    
    y_ticklabels = []

    for val in ax.get_yticks():
        y_ticklabels.append(round(val+0.50,1))

    

    ax.set_yticklabels(y_ticklabels, fontsize=PARAMS["fss"])
    
    title = "politicians_ideology_score.pdf"
    
    if savefig:
        fig.savefig(destinatio_plots_drivers + title, bbox_inches='tight')
