from app.observability import langfuse


def test_langfuse_connection():

    observation = langfuse.start_observation(
        name="test-observation"
    )

    print(observation)

    assert observation is not None

    langfuse.shutdown()
    
if __name__ == "__main__":
    test_langfuse_connection()