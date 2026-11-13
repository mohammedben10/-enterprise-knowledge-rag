"""
Automated Test Suite — Enterprise Knowledge RAG
-----------------------------------------------
Runs verified test queries against the knowledge base and validates
accurate grounding and source citation.
"""

import sys
from rag_engine import EnterpriseRAGEngine


def run_tests():
    print("=" * 70)
    print("🧪 Running Enterprise Knowledge RAG Test Suite")
    print("=" * 70)

    engine = EnterpriseRAGEngine()

    test_cases = [
        {
            "category": "Corporate Travel & Expenses",
            "question": "What is the policy for flights that are 6 or more hours long?",
            "expected_keywords": ["business", "premium economy", "6", "director"]
        },
        {
            "category": "HR & Parental Leave",
            "question": "How many weeks of paid leave do primary caregivers get, and what is the eligibility requirement?",
            "expected_keywords": ["16", "weeks", "90 days"]
        },
        {
            "category": "Finance & Procurement",
            "question": "What is the maximum purchase amount a Direct Manager can approve on their own?",
            "expected_keywords": ["1,000", "manager"]
        },
        {
            "category": "Customer Support SLA",
            "question": "What is the response time for a Priority 1 critical outage on the Enterprise Platinum tier?",
            "expected_keywords": ["15", "minutes", "platinum"]
        },
        {
            "category": "IT Security & Hardware",
            "question": "Are employees allowed to use personal laptops (BYOD) for production coding and accessing client data?",
            "expected_keywords": ["barred", "personal", "managed", "corporate", "not allowed"]
        }
    ]

    passed = 0
    total = len(test_cases)

    for i, test in enumerate(test_cases, start=1):
        print(f"\n[{i}/{total}] Testing: {test['category']}")
        print(f"❓ Question: {test['question']}")

        result = engine.query(test["question"])
        answer = result["answer"].lower()

        # Check keyword matches
        matches = [kw for kw in test["expected_keywords"] if kw.lower() in answer]
        has_sources = len(result.get("sources", [])) > 0

        print(f"💬 Answer Summary:\n   {result['answer'][:180]}...")
        print(f"📚 Sources Cited: {[s['file'] for s in result['sources']]}")

        if matches and has_sources:
            print(f"✅ PASSED (Matched concepts: {matches})")
            passed += 1
        else:
            print(f"⚠️ REVIEW (Matches found: {matches}, Sources found: {has_sources})")

    print("\n" + "=" * 70)
    print(f"📊 Test Results: {passed}/{total} Test Cases Passed Successfully!")
    print("=" * 70 + "\n")

    return passed == total


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
