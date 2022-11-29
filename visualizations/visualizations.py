from matplotlib import pyplot as plt
from drivers.configs.directories import Directories
import pandas as pd

""" Following script includes methods to recreate plots used in the report for this repository
"""

dir = Directories()
destination = str(dir.POLITIFACT_PLOTS_PATH) + "/" 
destination_plots_drivers = str(dir.PLOTS_PATH) + "/drivers/"

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
        fig.savefig(destination_plots_drivers + title, bbox_inches='tight')


def plot_top_news(x, y, labels, include_title=False, save_results=False):
    """
    Preprocess before input: convert your df to sort values ascendingly and specify the subset to plot with .tail(n)
    This takes in the top news from our 250 news sources derived through the Osmundsen et al. paper (2021).
    
    Args:
        x (lst): Number of occurances
        y (lst): Names of news medias
        include_title (bool, optional): if title should be included
        save_results (bool, optional): save results as pdf in the driver path.
    """

    colors = []
    color_dict = {'strong republican':'red',
                  'lean republican':'red',
                  'centrist':'grey',
                  'lean democratic': 'blue',
                  'strong democratic': 'blue'}
    
    
    
    for label in labels:
        colors.append(color_dict[label])


    plt.barh(y=y, width=x, color=colors, label=labels, alpha=0.9)

    plt.legend(['Democratic', 'Republican'])

    plt.yticks(fontsize=PARAMS['fss'])
    plt.xticks(fontsize=PARAMS['fss'], rotation=40, ha='right')
    plt.xlabel("Number of shares", fontsize=PARAMS['fsm'])
    #plt.ylabel("News outlet", fontsize=PARAMS['fsm'])
    
    
    if include_title:
        plt.title("Top shared" + len(x) + " news outlets", fontsize=PARAMS['fsl'])
        
    if save_results:
        plt.savefig(destination_plots_drivers + "top_news_shared.pdf", bbox_inches='tight')
    else:
        plt.show()



def plot_top_politicians_flw(x, y, labels, include_title=False, save_results=False):
    """
    Preprocess before input: convert your df to sort values ascendingly and specify the subset to plot with .tail(n)
    
    Args:
        x (lst): Number of occurances
        y (lst): Names of politicians
        labels (lst): the Party the politician is affiliated with.
        include_title (bool, optional): if title should be included
        save_results (bool, optional): save results as pdf in the driver path.
    """
    
    colors = []
    color_dict = {'Republican':'red',
                  'Democrat': 'blue'}

    for label in labels:
        colors.append(color_dict[label])

    plt.barh(y=y, width=x, color=colors, label=labels, alpha=0.9)

    plt.legend(['Democrat', 'Republican'])
    
    plt.yticks(fontsize=PARAMS['fss'])
    plt.xticks(fontsize=PARAMS['fss'], rotation=40, ha='right')
    plt.xlabel("Number of follows", fontsize=PARAMS['fsm'])
    #plt.ylabel("U.S. Politicians", fontsize=PARAMS['fsm'])
    
    
    if include_title:
        plt.title("Top shared" + len(x) + " politicians followed", fontsize=PARAMS['fsl'])
        
    if save_results:
        plt.savefig( destination_plots_drivers + "top_politicians_followed.pdf", bbox_inches='tight')
    else:
        plt.show()
        
        

def plot_politicians_vs_news_iscores(users_worldview_clean, savefig=False): 

    plt.figure(figsize=(8,6))

    cm = plt.cm.get_cmap('inferno')

    x = users_worldview_clean.ideology_score
    y = users_worldview_clean.ideology_score_flw
    c = users_worldview_clean.average_falsity_score


    sc = plt.scatter(x=x,y=y,c=c, vmin=0, vmax=1,cmap=cm, alpha=0.8)

    plt.xlabel("News ideology score", fontsize=13)
    plt.ylabel("Politicians followed ideology score", fontsize=13)

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    cbar = plt.colorbar(sc)

    cbar.set_label("Average falsity score", rotation=270, labelpad=20, fontsize=13)

    if savefig:
        plt.savefig(str(dir.PLOTS_PATH) + "/drivers/" + "politician_vs_news_iscores.pdf", bbox_inches='tight')
    else:
        plt.show()