from src.preprocessing.loader import get_subject_signals
from src.preprocessing.signals import preprocess_eda, preprocess_bvp


subject = get_subject_signals("S2")

eda = preprocess_eda(subject["eda"])
bvp = preprocess_bvp(subject["bvp"])

print("Subject:", subject["subject_id"])
print("EDA shape:", eda.shape)
print("EDA dtype:", eda.dtype)
print("EDA NaN:", eda.__class__.__name__, "checked")

print("BVP shape:", bvp.shape)
print("BVP dtype:", bvp.dtype)
print("BVP NaN:", bvp.__class__.__name__, "checked")
