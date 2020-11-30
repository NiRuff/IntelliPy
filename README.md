![IntelliPy Logo](https://user-images.githubusercontent.com/50486014/99252712-ad2d9c00-280f-11eb-994f-3149271e3e18.png)
# IntelliPy
## Python GUI for automatic analyses of IntelliCage data

### Motivation:

The IntelliCage system helps researchers to conduct behavioral experiments and learning experiments with mice while ensuring minimal human intervention. The animals can be observed for long time periods - up to several weeks. This long-term data acquisition can provide new insights in mouse behavior, that might not be detectable in short-term observations.
However, analyzing those big amounts of data is challenging for many researchers. 
IntelliPy aims to simplify and automize many aspects of the analysis, such as acquiring data per group, creating learning curves or pivoting parameters in different timeframes. All plots are automatically created and the final tables for statistical tests are stored separately for the user.

### Installation & Launch

#### ...using pip
IntelliPy can be installed in principal for every operating system running Python. The easiest way, is installing it via the Python Packaging Index (PyPI) using the command:

```pip install intellipy```

It can then be used with

```python3 -m intellipy``` or just ```python -m intellipy```

#### ...using the intelli.exe
If you have problems installing IntelliPy using pip, you can also download a windows exe file [here](https://seafile.rlp.net/f/a7f0d918b8fe44f6aadf/?dl=1). As there is no need to have Python or any packages (e.g. pandas) installed, this file is very big, as it brings python and all recommended packages with it.
Choosing the latter way for using IntelliPy, you just have to extract the *ZIP* file, open the directory and launch the *intelli.exe*.

### Usage

IntelliyPy utilizes the Nosepoke.txt and Visit.txt file of an experiment. These files can be extracted using the TSE Analyzer.
Additionally, a Group Assignment file has to be created:

![Usage](https://user-images.githubusercontent.com/50486014/99260095-3c8c7c80-281b-11eb-8d59-d9ec71e55747.png)

#### Create a group assignment file:
A tab-separated text file (tsv) is necessary in order to tell IntelliPy, which Animal belongs to which group.
It additionally contains information about the label given for sucrose - if Sucrose Preference experiments were performed.
You have to create this file for yourself in this manner:

1)  Give the word **Label** followed by a tab followed by the label you chose for sucrose in line one.
2)  Give the name of the first group followed by a tab and then all animals belonging to this group - also tab separated
3)  repeat step 2) for all remaining groups

*An example file is added as* **"Group_assignment.txt"**

### Conducted analyses:

![Analyses Overview](https://user-images.githubusercontent.com/50486014/99260101-3dbda980-281b-11eb-8760-6252db54acd3.png)

#### Pivot tables:
For the parameters, measured by the IntelliCage Systems, such as **Lick Duration, Nosepoke Number** or **NosepokeDuration**, pivot tables are created for each module by IntelliPy. By default, these timeframes are created per day, but the user can add more timeframes using the IntelliPy GUI, like e.g. 12-hour or 6-hour timeframes. For further sttistical analyses, the pivoting results are stored as CSV files.

#### Learning Rates:
As the experiments conducted with the IntelliCage systems can be conducted as learning experiments with different setups per phase, the learning rate of each individual as well as for the each group can be of high interest. Rather than only the final rate of correct attempts, the rate per hour and per visit is computed and plotted by IntelliPy. This enables the user, to utilize longitudinal learning information for each individual and group.
For those learning rates, it is even possible to include all nosepokes or to remove those that were not followed by a lick. It can be argued about, whether a nosepoe without a lick should or shouldn't be accounted as a correct attempt, so this decision is up to the user. Furthermoe, there are both, the possibility to exclude all nosepokes not followed by a lick or to treat them as incorrect attempts.

#### Sucrose Preference analyses:
For learning experiments, including the choice between water and sucrose, the proportion of LickDuration spent for Sucrose over time is computed by IntelliPy. Additionally, it is possible to define Sucrose and Water or just one of both as correct for the learning rate.

