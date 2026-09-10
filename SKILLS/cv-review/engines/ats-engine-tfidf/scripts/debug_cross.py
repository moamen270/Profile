from ats.matching.cross_encoder import CrossEncoderReranker
from ats.matching.embedding_match import SemanticMatcher
from ats.parsing.jd_parser import parse_job_description

jd = parse_job_description(
    "REQUIREMENTS\n- Strong Python and SQL skills\n- Kubernetes operations experience"
)
reranker = CrossEncoderReranker(__import__("ats.matching.embedding_match", fromlist=["SemanticMatcher"]).SemanticMatcher())

resume_good = "Expert in python and sql databases.\nManaged kubernetes clusters in production."
resume_bad = "Ballet dancer and pastry chef."

for name, resume in [("good", resume_good), ("bad", resume_bad)]:
    result = reranker.rerank(jd, resume)
    print(name, "->", result.score)
