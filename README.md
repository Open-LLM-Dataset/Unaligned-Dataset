# Unaligned Dataset
The goal of this project is to create an open-source and constantly evolving dataset of unaligned data for llm finetuning or even training. Community contributions will allow for the quality of the dataset to consistently increase which will be tracked by versioning the dataset after certain milestones. This will also make it easier to keep track of which version of the dataset was used for finetuning once they begin rolling out. Major versions will indicate changes in methodology of generatign initial data such as using a better model or a altering the prompt-reply generation scripts. Minor versions will be used to add human contributions for improving the inital synthetic data.

## Version 0.0.0
The initial data was created by having llama3-8b-instruct-q8_0 generate sets of 100 unaligned prompts until 256,000 were collected. Then, llama3-8b-instruct-q8_0 was used to generate responses to these unaligned prompts. The prompt reply pairs are saved in json format. This is meant to provide a starting point of how the project will look, this is NOT a good dataset for finetuning. Llama-3-8b is simply not powerful enough to provide decent quality data, even data that's only intended to be used as a starting point. It was used due to hardware limitations (RTX 3060) and a desire to create a quick hacky first implementation.

## Contributing 
Currently all of the data is synthetic which was necessary to achieve such scale with few resources. Looking foward, the goal is for individuals to read through the data and make contributions to improve it. Below is a guide for contributing:  

Contributions are divided into several categories:
1. Prompt/Reply Improvement
2. Deduplication
3. New Data

<details>
<summary>Prompt/Reply Improvement</summary>
<br>

The most difficult to define, but arguably most important part of improving the datasets. Manually reading through the generated prompt-reply pairs and improving them can include:
- Correcting factual errors
- Eliminating moralizing statements

</details>

<br>
<details>
<summary>Deduplication</summary>
<br>

A strong dataset means having a large variety of unique prompts. If you find two or more prompt/reply pairs which are very similar, make a pull request inicating the locations of the duplicates and remove all but the one percieved to be the highest quality. 

</details>
<br>
<details>
<summary>New Data</summary>
<br>

Add more data to the dataset by either generating more prompt-reply pairs using the provided python scripts (requires locally running ollama and respective model) or by hand writing new prompt-reply pairs, making sure to follow the appropriate format.

</details>

## Future Plans
- [ ] Complete v0 synthetic reply generation
- [ ] Analyze v0 data to identify improvements in pipeline (python scripts)
- [ ] Test models(Command-R-Plus, WizardLM-2-8x22B, Llama-3-70b) by producing 1000 sample responses to the same prompts to decide which should be used to create v1.0.0 synthetic base dataset
- [ ] Create a better way to edit replies than manually editing the json, markdown is not rendered properly in json, it's difficults to read long responses, and its easy to break the json if a quote/bracket/comma is accidentally deleted

## Models Created 
None yet

## Gitea Mirror
In case this repository is no longer avaliable through github, a mirror is being hosted using [gitea](https://20250123.xyz/dataset-creator/Unaligned-Dataset)
