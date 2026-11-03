from fbsc import FBSCEngine

engine = FBSCEngine()
result = engine.run_cycle(
    "Assess the claim, identify evidence, and state what remains uncertain."
)

print(result.message)
print("Completed phases:", [record.phase.label for record in result.records])
print("Output:", result.output)
