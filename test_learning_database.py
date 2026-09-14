from ai_engine.learning_database import LearningDatabase

db = LearningDatabase()

db.save({

    "test":"test_alarm",

    "root_cause":"Synchronization",

    "fix":"Use verify_alarm() polling"

})

print(db.load())