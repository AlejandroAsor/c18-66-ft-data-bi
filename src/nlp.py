from transformers import pipeline

# Definir las consultas y etiquetas
texts = [
    "Conocimientos: Experiencia en Backend (GO o Node.js) Indispensable.",
]
labels = ["programming language", "verb"]

# Usar el modelo 'facebook/bart-large-mnli'
classifier_bart = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')

# Usar el modelo 'roberta-large-mnli'
classifier_roberta = pipeline("zero-shot-classification", model="roberta-large-mnli")

print("Resultados usando BART:")
for text in texts:
    result_bart = classifier_bart(text, candidate_labels=labels, hypothesis_template="This text is about {}.")
    print(f"Texto original: {text}\nResultado BART: {result_bart}\n")

print("Resultados usando RoBERTa:")
for text in texts:
    result_roberta = classifier_roberta(text, candidate_labels=labels, hypothesis_template="This text is about {}.")
    print(f"Texto original: {text}\nResultado RoBERTa: {result_roberta}\n")



# from transformers import pipeline
#
# # Definir las consultas y etiquetas
# texts = [
#     """
# Ingeniero de Sistemas Senior Inglés Avanzado
#
# Bogotá
#
# Agencia de empleo de Colsubsidio
#
# Bogotá, D.C., Bogotá, D.C.
#
# Empresa verificada
#
# Agencia de empleo de Colsubsidio logo
# Postularme
#
#
#
#
# Contrato a término indefinido
#
# Tiempo Completo
#
# Presencial
#
# Empresa requiere Ing en Sistemas, Informatica o carreras afines:
#
# -Experiencia mínima de 5 años en diseño, implementación y mantenimiento pipelines automatizadas de compilación y despliegue.
# Manejo de TFS Admin, Azure DevOps, Proget/Nuget, SVN admin, Docker, Github access support e Installshield. Administración de recursos en Microsoft Azure.
# Conocimiento de ProGet o Visual SVN.
# Dominio de lenguajes Python o Shell.
# Exp con Jenkins, TeamCity y sistemas de control de versiones (Git).
# Exp con Docker o Kubernetes.
# Conocimiento de Ansible o Puppet.
#
# -Salario entre 12 a 15 SMLV.
# -Contrato a término indefinido.
# -Lugar de trabajo Bogotá presencial.
# Requerimientos
#
# Educación mínima: Universidad / Carrera Profesional
# 5 años de experiencia
# Conocimientos: Python, Shell, Docker
#     """
# ]
# labels = ["Tecnología", "No Tecnología"]
#
# # Usar el modelo 'facebook/bart-large-mnli'
# classifier_bart = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
#
# # Usar el modelo 'roberta-large-mnli'
# classifier_roberta = pipeline("zero-shot-classification", model="roberta-large-mnli")
#
# print("Resultados usando BART:")
# for text in texts:
#     result_bart = classifier_bart(text, candidate_labels=labels, hypothesis_template="This job posting is related to {}.")
#     print(f"Texto original: {text}\nResultado BART: {result_bart}\n")
#
# print("Resultados usando RoBERTa:")
# for text in texts:
#     result_roberta = classifier_roberta(text, candidate_labels=labels, hypothesis_template="This job posting is related to {}.")
#     print(f"Texto original: {text}\nResultado RoBERTa: {result_roberta}\n")
#
#
#





# from transformers import (BertForSequenceClassification, BertTokenizer,
#                           RobertaForSequenceClassification, RobertaTokenizer,
#                           DistilBertForSequenceClassification, DistilBertTokenizer,
#                           XLNetForSequenceClassification, XLNetTokenizer,
#                           AlbertForSequenceClassification, AlbertTokenizer,
#                           ElectraForSequenceClassification, ElectraTokenizer,
#                           DebertaForSequenceClassification, DebertaTokenizer,
#                           FlaubertForSequenceClassification, FlaubertTokenizer,
#                           CamembertForSequenceClassification, CamembertTokenizer,
#                           BartForSequenceClassification, BartTokenizer)
# import numpy as np
# import torch
#
# # Definir los nombres de los modelos
# model_names = [
#     "bert-base-uncased",
#     "roberta-base",
#     "distilbert-base-uncased",
#     "xlnet-base-cased",
#     "albert-base-v2",
#     "google/electra-base-discriminator",
#     "microsoft/deberta-base",
#     "flaubert/flaubert_base_cased",
#     "camembert-base",
#     "facebook/bart-base"
# ]
#
# # Definir las clases de modelos y tokenizers
# model_classes = [
#     BertForSequenceClassification,
#     RobertaForSequenceClassification,
#     DistilBertForSequenceClassification,
#     XLNetForSequenceClassification,
#     AlbertForSequenceClassification,
#     ElectraForSequenceClassification,
#     DebertaForSequenceClassification,
#     FlaubertForSequenceClassification,
#     CamembertForSequenceClassification,
#     BartForSequenceClassification
# ]
#
# tokenizer_classes = [
#     BertTokenizer,
#     RobertaTokenizer,
#     DistilBertTokenizer,
#     XLNetTokenizer,
#     AlbertTokenizer,
#     ElectraTokenizer,
#     DebertaTokenizer,
#     FlaubertTokenizer,
#     CamembertTokenizer,
#     BartTokenizer
# ]
#
# # Cargar los modelos y tokenizers
# models = []
# tokenizers = []
#
# for model_name, model_class, tokenizer_class in zip(model_names, model_classes, tokenizer_classes):
#     try:
#         tokenizer = tokenizer_class.from_pretrained(model_name)
#         model = model_class.from_pretrained(model_name, num_labels=2)
#         tokenizers.append(tokenizer)
#         models.append(model)
#         print(f"Modelo y tokenizer cargados: {model_name}")
#     except Exception as e:
#         print(f"Error cargando {model_name}: {e}")
#
# # Función para predecir usando ensemble
# def ensemble_predict(text, models, tokenizers):
#     inputs = [tokenizer(text, return_tensors="pt", truncation=True, padding=True) for tokenizer in tokenizers]
#     probs = []
#     with torch.no_grad():
#         for i, model in enumerate(models):
#             logits = model(**inputs[i]).logits
#             probs.append(torch.softmax(logits, dim=1).numpy())
#     avg_probs = np.mean(probs, axis=0)
#     return avg_probs.argmax(), avg_probs
#
# # Ejemplo de uso
# text = "Tecnico Mecácnico C"
# label, prob = ensemble_predict(text, models, tokenizers)
# labels = ["others", "programming language"]
#
# print(f"Texto: {text}")
# print(f"Clasificación: {labels[label]}")
# print(f"Probabilidades: {prob}")
