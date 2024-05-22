# Unaligned Dataset
The goal of this project is to create an open-source and constantly evolving dataset of unaligned data for llm finetuning or even training. Community contributions will allow for the quality of the dataset to consistently increase which will be tracked by versioning the dataset after certain milestones. This will also make it easier to keep track of which version of the dataset was used for finetuning once they begin rolling out.

## Initial Data
The initial data(v0.0.0) was created by having llama3-8b-instruct-q8_0 generate sets of 100 unaligned prompts until 256,000 were collected. Then, llama3-8b-instruct-q8_0 was used to generate responses to these unaligned prompts. The prompt reply pairs are saved in json format.

## Contributing 
Currently all of the data is synthetic which was necessary to achieve such scale with few resources. Looking foward, the goal is for individuals to read through the data and make contributions to improve it. Below is a guide for contributing:  

Contributions are divided into several categories:
1. Prompt/Reply Improvement
2. Deduplication
3. New Data

<details>
<summary>Promt/Reply Improvement</summary>
<br>
Text
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
Text
</details>

## Models Created 
None yet