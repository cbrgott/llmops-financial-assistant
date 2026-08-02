from app.observability import langfuse

observation = langfuse.start_observation(
    name="test-observation"
)

print(observation)

langfuse.shutdown()

print("Done")