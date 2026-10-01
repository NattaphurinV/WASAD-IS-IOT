from src.preprocessing.loader import get_subject_signals


subject = get_subject_signals("S2")

print("Subject:", subject["subject_id"])
print("EDA shape:", subject["eda"].shape)
print("BVP shape:", subject["bvp"].shape)
print("Label shape:", subject["label"].shape)
