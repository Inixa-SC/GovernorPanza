from datasets import load_dataset

dataset_name = "CyberNative/Code_Vulnerability_Security_DPO"
dataset = load_dataset(dataset_name)

only_prompts = dataset['train'].select_columns(["question","lang"])

only_prompts.to_csv("datasets/questions_only.csv")

