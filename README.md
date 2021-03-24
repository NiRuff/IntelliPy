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
If you have problems installing IntelliPy using pip, you can also download a windows exe file [here](https://seafile.rlp.net/repo/e0e11fef-b403-428a-bfcd-4fd58983f889/3d1f4cbec020c290e9c7d26244669f798e20c33b/download/?file_name=intellipy.zip&p=%2Fintellipy.zip). As there is no need to have Python or any packages (e.g. pandas) installed, this file is quite big (75MB unzipped), as it brings Python and all recommended packages with it.
Choosing the latter way for using IntelliPy, you just have to extract the *ZIP* file, open the directory and launch the *intelli.exe*.

### Settings

IntelliPy utilizes the Nosepoke.txt, Visit.txt and Animal.txt file of an IntelliCage experiment. These files can be extracted using the TSE Analyzer. Additionally, if new groups should be assigned that are not included in the Animal.txt file, a group assignment file can be created, in order to conduct new group-wise analyses or to specify the alternative side conditions such as "Sucrose" or any other user-defined label for e.g. sucrose preference experiments:

![Usage](https://user-images.githubusercontent.com/50486014/112329058-243fd900-8cb7-11eb-990a-d3e3e2f42795.png)

#### Create a group assignment file:
A tab-separated text file (tsv) can be used instead of the Animal.txt file for assigning new animal-group relationships. To address experiments with multiple conditions per animal, it is possible to relate an animal to more than one group. The group assignment file additionally contains information about the alternative label (if used). If such alternative labels were used in the IntelliCage experiment and are thus provided by the user in the group assignment file, the options when starting IntelliPy adjust, so that the user can chosose, how to treat this alternative label. The group assignment file can be created as follows:

1)  Give the word **Label** followed by a tab followed by the alternative labelused in the experiment.
2)  Give the name of the first group followed by a tab and then all animals belonging to this group - also tab separated
3)  repeat step 2) for all remaining groups

*An example file is added as* **"Group_assignment.txt"**

### Conducted analyses:

![Analyses Overview](https://user-images.githubusercontent.com/50486014/99260101-3dbda980-281b-11eb-8760-6252db54acd3.png)

#### Pivot tables:
For the parameters, measured by the IntelliCage Systems, such as **Lick Duration, Nosepoke Number** or **NosepokeDuration**, pivot tables are created for each module by IntelliPy. By default, these timeframes are created per day, but the user can add more timeframes using the IntelliPy GUI, like e.g. 12-hour or 6-hour timeframes. For further statistical analyses, the pivoting results are stored in the resulting xlsx files.

#### Learning Rates:
As the experiments conducted with the IntelliCage systems can be conducted as learning experiments with different setups per phase, the learning rate of each individual as well as for the each group can be of high interest. Rather than only the final rate of correct attempts, the rate per hour and per visit is computed and plotted by IntelliPy. This enables the user, to utilize longitudinal learning information for each individual and group.
For those learning rates, it is even possible to include all nosepokes or to remove those that were not followed by a lick. It can be argued about, whether a nosepoe without a lick should or shouldn't be accounted as a correct attempt, so this decision is up to the user. Furthermore, there are both, the possibility to exclude all nosepokes not followed by a lick or to treat them as incorrect attempts.

#### Alternative Label Analyses (e.g. Sucrose preference):
For learning experiments, including the choice between two sides after choosing the correct place, such as the choice between one side with Sucrose and one with Water, the proportion of Lick Duration spent for one side rather than the other side over time is computed by IntelliPy. Additionally, it is possible to define the alternative label (e.g. "Sucrose") as correct or as incorrect for the learning rate computation. This will influence the computation of the learning rate of the sucrose preference experiments. Consequently, for learning modules utilizing an alternative label, the nosepoke learning rate files are influenced by the used option and one additional file is created for showing the lick duration ratio between the "alternative label" side and the "Correct" side.

### Output files
...
