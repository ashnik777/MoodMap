-- Populating the Company table
INSERT INTO Company (Name) VALUES
    ('AmeriaBank'),
    ('AcbaBank'),
    ('Krisp');

-- Populating the Agent table
INSERT INTO Agent (RegistrationDate, Username, CompanyId) VALUES
    ('2023-01-01', 'John', 1),
    ('2023-02-01', 'Karen', 1),
    ('2023-03-01', 'David', 1);

-- Populating the Call table
INSERT INTO Call (CallId, StartTime, EndTime, AgentId, CallScore, Duration) VALUES
    (1, '2023-01-01 08:00:00', '2023-01-01 08:05:00', 1, 80, 300),
    (2, '2023-01-02 09:00:00', '2023-01-02 09:03:00', 1, 85, 180),
    (3, '2023-01-03 10:00:00', '2023-01-03 10:04:00', 3, 90, 240);

-- Populating the CallInfo table
INSERT INTO CallInfo (CallId, Topic, ClientInterrupts, AgentInterrupts, SilencePercent, ClientSpeechDuration, AgentSpeechDuration, client_hatespeechpercent, agent_hatespeechpercent, client_ironypercent, agent_ironypercent, customer_satisfaction_rate, agent_performance_rate, alert, satisfied) VALUES
    (1, 'Sales', 1, 1, 10, 150, 140, 5, 3, 2, 1, 80, 85, 0, 1),
    (2, 'Support', 1, 0, 5, 120, 75, 3, 2, 1, 0, 85, 90, 1, 1),
    (3, 'Complaint', 0, 0, 15, 100, 125, 7, 4, 3, 2, 90, 95, 1, 1);

-- Populating the Call_Mood_Agent table
INSERT INTO Call_Mood_Agent (CallId, StartTime, EndTime, Emotion, emotion_in_number) VALUES
    (1, '2023-01-01 08:00:00', '2023-01-01 08:15:00', 'Happy', 4),
    (1, '2023-01-02 09:00:10', '2023-01-02 09:15:00', 'Neutral', 3),
    (1, '2023-01-03 10:00:20', '2023-01-03 10:15:00', 'Angry', 1),
    (1, '2023-01-01 08:00:30', '2023-01-01 08:15:00', 'Happy', 4),
    (1, '2023-01-02 09:00:40', '2023-01-02 09:15:00', 'Neutral', 3),
    (1, '2023-01-03 10:00:50', '2023-01-03 10:15:00', 'Angry', 1),
    (1, '2023-01-01 08:00:41', '2023-01-01 08:15:00', 'Happy', 4),
    (1, '2023-01-02 09:00:01', '2023-01-02 09:15:00', 'Neutral', 3),
    (2, '2023-01-03 10:00:02', '2023-01-03 10:15:00', 'Angry', 1),
    (2, '2023-01-01 08:00:03', '2023-01-01 08:15:00', 'Happy', 4),
    (2, '2023-01-02 09:00:04', '2023-01-02 09:15:00', 'Neutral', 3),
    (2, '2023-01-03 10:00:05', '2023-01-03 10:15:00', 'Sad', 2),
    (2, '2023-01-01 08:00:06', '2023-01-01 08:15:00', 'Happy', 4),
    (2, '2023-01-02 09:00:07', '2023-01-02 09:15:00', 'Neutral', 3),
    (2, '2023-01-03 10:00:08', '2023-01-03 10:15:00', 'Angry', 1);

-- Populating the Call_Mood_Client table
INSERT INTO Call_Mood_Client (CallId, StartTime, EndTime, Emotion, emotion_in_number) VALUES
    (1, '2023-01-01 08:00:00', '2023-01-01 08:15:00', 'Happy', 4),
    (1, '2023-01-02 09:00:10', '2023-01-02 09:15:00', 'Neutral', 3),
    (1, '2023-01-03 10:00:20', '2023-01-03 10:15:00', 'Angry', 1),
    (1, '2023-01-01 08:00:30', '2023-01-01 08:15:00', 'Happy', 4),
    (1, '2023-01-02 09:00:40', '2023-01-02 09:15:00', 'Neutral', 3),
    (1, '2023-01-03 10:00:50', '2023-01-03 10:15:00', 'Angry', 1),
    (1, '2023-01-01 08:00:41', '2023-01-01 08:15:00', 'Happy', 4),
    (1, '2023-01-02 09:00:01', '2023-01-02 09:15:00', 'Neutral', 3),
    (2, '2023-01-03 10:00:02', '2023-01-03 10:15:00', 'Angry', 1),
    (2, '2023-01-01 08:00:03', '2023-01-01 08:15:00', 'Happy', 4),
    (2, '2023-01-02 09:00:04', '2023-01-02 09:15:00', 'Neutral', 3),
    (2, '2023-01-03 10:00:05', '2023-01-03 10:15:00', 'Sad', 2),
    (2, '2023-01-01 08:00:06', '2023-01-01 08:15:00', 'Happy', 4),
    (2, '2023-01-02 09:00:07', '2023-01-02 09:15:00', 'Neutral', 3),
    (2, '2023-01-03 10:00:08', '2023-01-03 10:15:00', 'Angry', 1);

-- Populating the Call_Sentence_Agent table
INSERT INTO Call_Sentence_Agent (CallId, SpeechText, Sentiment, Irony, StartTime, EndTime, HateLevelPercent, MeanEmotion) VALUES
    (1, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:03', '2023-01-01 08:05:00', 0, 'Happy'),
    (1, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:20', 0, 'Neutral'),
    (1, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:04', '2023-01-01 08:05:00', 0, 'Happy'),
    (1, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:50', 0, 'Neutral'),
    (1, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:06', '2023-01-01 08:05:00', 0, 'Happy'),
    (2, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:07', 0, 'Neutral'),
    (2, 'I understand your frustration. Let me try to resolve this issue for you.', 'Negative', 'None', '2023-01-03 10:00:08', '2023-01-03 10:05:00', 10, 'Angry'),
    (2, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:00', '2023-01-01 08:05:09', 0, 'Happy'),
    (2, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:13', 0, 'Neutral'),
    (2, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:00', '2023-01-01 08:05:14', 0, 'Happy'),
    (2, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:30', 0, 'Neutral');

-- Populating the Call_Sentence_Client table
INSERT INTO Call_Sentence_Client (CallId, SpeechText, Sentiment, Irony, StartTime, EndTime, HateLevelPercent, MeanEmotion) VALUES
    (1, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:03', '2023-01-01 08:05:00', 0, 'Happy'),
    (1, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:20', 0, 'Neutral'),
    (1, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:04', '2023-01-01 08:05:00', 0, 'Happy'),
    (1, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:50', 0, 'Neutral'),
    (1, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:06', '2023-01-01 08:05:00', 0, 'Happy'),
    (2, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:07', 0, 'Neutral'),
    (2, 'I understand your frustration. Let me try to resolve this issue for you.', 'Negative', 'None', '2023-01-03 10:00:08', '2023-01-03 10:05:00', 10, 'Angry'),
    (2, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:00', '2023-01-01 08:05:09', 0, 'Happy'),
    (2, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:13', 0, 'Neutral'),
    (2, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:00', '2023-01-01 08:05:14', 0, 'Happy'),
    (2, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:30', 0, 'Neutral');

-- Populating the Call_Sentence_Aspect_Agent table
INSERT INTO Call_Sentence_Aspect_Agent (CallSentenceId, Aspect, Sentiment, Opinion) VALUES
    (1, 'Customer account6', 'Positive', 'Resolve issue'),
    (1, 'Internet connection2', 'Neutral', 'Assistance'),
    (1, 'Customer account1', 'Positive', 'Resolve issue'),
    (1, 'Internet connection3', 'Neutral', 'Assistance'),
    (2, 'Service qualitys', 'Negative', 'Understand frustration'),
    (2, 'Service qualityq', 'Negative', 'Understand frustration'),
    (2, 'Service qualityw', 'Negative', 'Understand frustration'),
    (3, 'Service qualityr', 'Negative', 'Understand frustration'),
    (3, 'Service qualityt', 'Negative', 'Understand frustration'),
    (3, 'Service quality5', 'Negative', 'Understand frustration');

-- Populating the Call_Sentence_Aspect_Client table
INSERT INTO Call_Sentence_Aspect_Client (CallSentenceId, Aspect, Sentiment, Opinion) VALUES
    (1, 'Customer account6', 'Positive', 'Resolve issue'),
    (1, 'Internet connection2', 'Neutral', 'Assistance'),
    (1, 'Customer account1', 'Positive', 'Resolve issue'),
    (1, 'Internet connection3', 'Neutral', 'Assistance'),
    (2, 'Service qualitys', 'Negative', 'Understand frustration'),
    (2, 'Service qualityq', 'Negative', 'Understand frustration'),
    (2, 'Service qualityw', 'Negative', 'Understand frustration'),
    (3, 'Service qualityr', 'Negative', 'Understand frustration'),
    (3, 'Service qualityt', 'Negative', 'Understand frustration'),
    (3, 'Service quality5', 'Negative', 'Understand frustration');
