<img src="res/tutorial/logo_orig.png" style="float:left; width:32px;"/>

# ASNRVis

ASNViz is a multimedia analytics solution that facilitates the visualization and analysis of animal social networks (ASNs). By modeling ASNs as networks of nodes and edges, ASNViz provides valuable insights into the dynamics and evolution of animal communities. The tool quantifies and visualizes the social structure at node and network levels, predicts future interactions when new individuals are added using deep-learning, and allows for manual updates based on empirical observations.

<center>
<img src="res/example_screenshot.png" style="width: 60%; max-width: 600px;"/>
</center>

## Installation Guide

Our solution does not require the use of GPU, enabling plug and play accessibility to a wide range of computer setups.

### Step 1: Clonining
This repository consists the [asnr](https://github.com/bansallab/asnr) repository as a submodule, therefore you will need recurisve strategy:
```
git clone --recursive git@github.com:madhurapawaruva/animalsocialnw_team7.git
cd animalsocialnw_team7
```
If you have already cloned the repository, you can also download the submodule afterwards:
```
git submodule update --init
```

### Step 2: Environment

Conda:
```
conda env create -f env.yml
conda activate t7ma
```
Pip:
```
pip install -r requirements.txt
```

## Run
```
python app.py
```

## Available social graphs

| Taxonomy | Animal Name    | Image                                                                                                         |
| -------- | -------------- | ------------------------------------------------------------------------------------------------------------- |
| Aves     | barnswallow    | <img src="./res/animal_intro/images/barnswallow_association_weighted.jpg" width="64" height="64" />           |
| Aves     | songbird       | <img src="./res/animal_intro/images/songbird_association_weighted.jpg" width="64" height="64" />              |
| Aves     | sparrow        | <img src="./res/animal_intro/images/sparrow_flockmembership_weighted.jpg" width="64" height="64" />           |
| Insecta  | ants           | <img src="./res/animal_intro/images/ants_proximity_weighted.jpg" width="64" height="64" />                    |
| Insecta  | beetle         | <img src="./res/animal_intro/images/beetle_proximity_weighted.jpg" width="64" height="64" />                  |
| Mammalia | baboon         | <img src="./res/animal_intro/images/baboon_association_weighted.jpg" width="64" height="64" />                |
| Mammalia | bats           | <img src="./res/animal_intro/images/bats_foodsharing_weighted.jpg" width="64" height="64" />                  |
| Mammalia | bison          | <img src="./res/animal_intro/images/bison_dominance_weighted.jpg" width="64" height="64" />                   |
| Mammalia | groundsquirrel | <img src="./res/animal_intro/images/groundsquirrel_association_weighted.jpg" width="64" height="64" />        |
| Mammalia | mouse          | <img src="./res/animal_intro/images/mouse_social_projection_bipartite_weighted.jpg" width="64" height="64" /> |
| Mammalia | rhesusmacaque  | <img src="./res/animal_intro/images/rhesusmacaque_association_weighted.jpg" width="64" height="64" />         |


| Aves                                                                                                | Insecta                                                                                    | Mammalia                                                                                       | Mammalia                                                                                     | Insecta                                                                                      | Mammalia                                                                                    | Aves                                                                                                   | Mammalia                                                                                                      | Mammalia                                                                                              | Aves                                                                                             | Aves                                                                                                |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| barnswallow                                                                                         | ants                                                                                       | baboon                                                                                         | bats                                                                                         | beetle                                                                                       | bison                                                                                       | groundsquirrel                                                                                         | mouse                                                                                                         | rhesusmacaque                                                                                         | songbird                                                                                         | sparrow                                                                                             |
| <img src="./res/animal_intro/images/barnswallow_association_weighted.jpg" width="64" height="64" /> | <img src="./res/animal_intro/images/ants_proximity_weighted.jpg" width="64" height="64" /> | <img src="./res/animal_intro/images/baboon_association_weighted.jpg" width="64" height="64" /> | <img src="./res/animal_intro/images/bats_foodsharing_weighted.jpg" width="64" height="64" /> | <img src="./res/animal_intro/images/beetle_proximity_weighted.jpg" width="64" height="64" /> | <img src="./res/animal_intro/images/bison_dominance_weighted.jpg" width="64" height="64" /> | <img src="./res/animal_intro/images/groundsquirrel_association_weighted.jpg" width="64" height="64" /> | <img src="./res/animal_intro/images/mouse_social_projection_bipartite_weighted.jpg" width="64" height="64" /> | <img src="./res/animal_intro/images/rhesusmacaque_association_weighted.jpg" width="64" height="64" /> | <img src="./res/animal_intro/images/songbird_association_weighted.jpg" width="64" height="64" /> | <img src="./res/animal_intro/images/sparrow_flockmembership_weighted.jpg" width="64" height="64" /> |
