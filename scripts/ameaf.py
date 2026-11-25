"""Claim-specific logical rule; not a validated certainty instrument."""
from itertools import product

REQUIREMENTS = {
    "adaptive_agency": "C",
    "observed_advantage": "CE",
    "causal_improvement": "CEA",
    "system_preference": "EN",
    "agent_net_benefit": "CEAN",
}
STATES = ("S","P","U","X","NA")

def support(claim, profile):
    required = REQUIREMENTS[claim]
    if set(profile) != set("CEAN") or any(v not in STATES for v in profile.values()):
        raise ValueError("Invalid profile")
    if any(profile[d] == "NA" for d in required):
        raise ValueError("Required dimension cannot be NA")
    return int(all(profile[d] == "S" for d in required))

def exhaustive_check():
    valid = supported = 0
    for claim, required in REQUIREMENTS.items():
        for values in product(STATES, repeat=4):
            p = dict(zip("CEAN", values))
            if any(p[d]=="NA" for d in required):
                continue
            valid += 1
            result = support(claim,p)
            assert result == (sum(p[d]=="S" for d in required)==len(required))
            supported += result
    return {"valid_profiles":valid,"supported_profiles":supported,"status":"logical verification only"}

if __name__ == "__main__":
    print(exhaustive_check())
