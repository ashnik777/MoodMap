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
INSERT INTO Call (StartTime, EndTime, AgentId, CallScore, Duration) VALUES
    ('2023-01-01 08:00:00', '2023-01-01 08:05:00', 1, 80, 300),
    ('2023-01-02 09:00:00', '2023-01-02 09:03:00', 1, 85, 180),
    ('2023-01-03 10:00:00', '2023-01-03 10:04:00', 3, 90, 240),
    ('2023-01-04 08:00:00', '2023-01-01 08:05:00', 1, 80, 300),
    ('2023-01-05 09:00:00', '2023-01-02 09:03:00', 1, 85, 180),
    ('2023-01-06 10:00:00', '2023-01-03 10:04:00', 3, 90, 240),
    ('2023-01-07 08:00:00', '2023-01-01 08:05:00', 1, 80, 300),
    ('2023-01-08 09:00:00', '2023-01-02 09:03:00', 1, 85, 180),
    ('2023-01-09 10:00:00', '2023-01-03 10:04:00', 3, 90, 240);

-- Populating the CallInfo table
INSERT INTO CallInfo (CallId, Topic, ClientInterrupts, AgentInterrupts, SilencePercent, ClientSpeechDuration, AgentSpeechDuration, client_hatespeechpercent, agent_hatespeechpercent, client_ironypercent, agent_ironypercent, customer_satisfaction_rate, agent_performance_rate, alert,togetherSpokenTime) VALUES
    (1, 'Sales',       1, 2, 10, 150,  140, 10, 30, 12, 11, 20, 65, False,12),
    (2, 'Support',     0, 4, 5, 120,   75,  30, 20, 11, 10, 10, 45, False,23),
    (3, 'Card',        4, 1, 15, 100,  125, 70, 40, 32, 22, 30, 50, True,34),
    (4, 'Sales',       6, 6, 20, 150,  140, 13, 32, 22, 1, 45, 90, False,54),
    (5, 'Support',     5, 3, 25, 120,  75,  24, 12, 13, 0, 55, 11, True,12),
    (6, 'transaction', 0, 4, 35, 100, 125,  65, 42, 34, 23, 76, 34, True,43),
    (7, 'Sales',        1, 1, 10, 150, 140, 23, 13, 21, 11, 34, 22, False,43),
    (8, 'bank account', 1, 5, 22, 120, 75,  12, 22, 12, 21, 98, 76, True,65),
    (9, 'card',         0, 0, 43, 100, 125, 7,  4,   3, 2,  90,  81, False,65);
-- Populating the Call_Mood_Agent table
INSERT INTO Call_Mood_Agent (CallId, Calculated, Emotion) VALUES
    (1, '2023-01-01 08:00:00', 'Happy'),
    (1, '2023-01-02 09:00:10', 'Neutral'),
    (1, '2023-01-01 08:00:30', 'Happy'),
    (1, '2023-01-02 09:00:40', 'Neutral'),
    (1, '2023-01-03 10:00:50', 'Angry'),
    (1, '2023-01-03 10:00:20', 'Angry'),
    (1, '2023-01-01 08:00:41', 'Happy'),
    (1, '2023-01-02 09:00:01', 'Neutral'),
    (2, '2023-01-03 10:00:02', 'Angry'),
    (2, '2023-01-01 08:00:03', 'Happy'),
    (2, '2023-01-02 09:00:04', 'Neutral'),
    (2, '2023-01-03 10:00:05', 'Sad'),
    (2, '2023-01-01 08:00:06', 'Happy'),
    (2, '2023-01-02 09:00:07', 'Neutral'),
    (2, '2023-01-03 10:03:08', 'Angry'),
    (3, '2023-01-01 08:04:00', 'Happy'),
    (3, '2023-01-02 09:05:11', 'Neutral'),
    (3, '2023-01-03 10:06:22', 'Angry'),
    (3, '2023-01-01 08:07:33', 'Happy'),
    (3, '2023-01-02 09:08:44', 'Neutral'),
    (3, '2023-01-03 10:00:55', 'Angry'),
    (3, '2023-01-01 08:09:46', 'Happy'),
    (3, '2023-01-02 09:08:07', 'Neutral'),
    (4, '2023-01-03 10:07:08', 'Angry'),
    (4, '2023-01-01 08:06:03', 'Happy'),
    (4, '2023-01-02 09:05:09', 'Neutral'),
    (4, '2023-01-03 10:04:00', 'Sad'),
    (4, '2023-01-01 08:03:09', 'Happy'),
    (4, '2023-01-02 09:02:08', 'Neutral'),
    (4, '2023-01-03 10:01:07', 'Angry');

-- Populating the Call_Mood_Client table
INSERT INTO Call_Mood_Client (CallId, Calculated, Emotion) VALUES
    (1, '2023-01-01 08:00:00', 'Happy'),
    (1, '2023-01-02 09:00:10', 'Happy'),
    (1, '2023-01-03 10:00:20', 'Angry'),
    (1, '2023-01-01 08:00:30', 'Happy'),
    (1, '2023-01-02 09:00:40', 'Happy'),
    (1, '2023-01-03 10:00:50', 'Angry'),
    (1, '2023-01-01 08:00:41', 'Angry'),
    (1, '2023-01-02 09:00:01', 'Neutral'),
    (2, '2023-01-03 10:00:02', 'Neutral'),
    (2, '2023-01-01 08:00:03', 'Sad'),
    (2, '2023-01-02 09:00:04', 'Neutral'),
    (2, '2023-01-03 10:00:05', 'Sad'),
    (2, '2023-01-01 08:00:06', 'Neutral'),
    (2, '2023-01-02 09:00:07', 'Neutral'),
    (2, '2023-01-03 10:03:08', 'Angry'),
    (3, '2023-01-01 08:04:00', 'Happy'),
    (3, '2023-01-02 09:05:11', 'Neutral'),
    (3, '2023-01-03 10:06:22', 'Happy'),
    (3, '2023-01-01 08:07:33', 'Happy'),
    (3, '2023-01-02 09:08:44', 'Neutral'),
    (3, '2023-01-03 10:00:55', 'Sad'),
    (3, '2023-01-01 08:09:46', 'Neutral'),
    (3, '2023-01-02 09:08:07', 'Sad'),
    (4, '2023-01-03 10:07:08', 'Angry'),
    (4, '2023-01-01 08:06:03', 'Happy'),
    (4, '2023-01-02 09:05:09', 'Neutral'),
    (4, '2023-01-03 10:04:00', 'Happy'),
    (4, '2023-01-01 08:03:09', 'Sad'),
    (4, '2023-01-02 09:02:08', 'Neutral'),
    (4, '2023-01-03 10:01:07', 'Angry');

-- Populating the Call_Sentence_Agent table
INSERT INTO Call_Sentence_Agent (CallId, SpeechText, Sentiment, Irony, StartTime, EndTime, HateLevelPercent, MeanEmotion) VALUES
    (1, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:03', '2023-01-01 08:00:10', 0, 'Happy'),
    (1, 'How may I assist you today?', 'Neutral', 'None', '2023-01-01 08:00:17', '2023-01-01 08:00:20', 0, 'Neutral'),
    (1, 'I will fix it now?', 'Positive', 'None', '2023-01-01 08:00:27', '2023-01-01 08:00:32', 0, 'Sad'),
    (1, 'you are welcome?', 'Negative', 'None', '2023-01-01 08:00:37', '2023-01-01 08:00:44', 0, 'Neutral'),

    (2, 'How may I assist you today?', 'Positive', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:07', 0, 'Neutral'),
    (2, 'I understand your frustration. Let me try to resolve this issue for you.', 'Negative', 'None', '2023-01-03 10:00:08', '2023-01-03 10:05:00', 10, 'Angry'),
    (2, 'Thank you for calling. How can I help you today?', 'Negative', 'None', '2023-01-01 08:00:00', '2023-01-01 08:05:09', 0, 'Happy'),
    (2, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:13', 0, 'Neutral'),
    (2, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:00', '2023-01-01 08:05:14', 0, 'Sad'),
    (2, 'How may I assist you today?', 'Negative', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:30', 0, 'Neutral');

-- Populating the Call_Sentence_Client table
INSERT INTO Call_Sentence_Client (CallId, SpeechText, Sentiment, Irony, StartTime, EndTime, HateLevelPercent, MeanEmotion) VALUES
    (1, 'Hi I have problem connected with my card?', 'Neutral', 'None', '2023-01-01 08:00:11', '2023-01-01 08:00:15', 0, 'Sad'),
    (1, 'How to fix my card problem?', 'Neutral', 'None', '2023-01-01 08:00:20', '2023-01-01 08:00:25', 0, 'Neutral'),
    (1, 'Thank you for fixing', 'Positive', 'None', '2023-01-01 08:00:33', '2023-01-01 08:00:36', 0, 'Happy'),
    (1, 'good by', 'Negative', 'None', '2023-01-01 08:00:45', '2023-01-01 08:00:50', 0, 'Neutral'),

    (2, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:07', 0, 'Neutral'),
    (2, 'I understand your frustration. Let me try to resolve this issue for you.', 'Negative', 'None', '2023-01-03 10:00:08', '2023-01-03 10:05:00', 10, 'Angry'),
    (2, 'Thank you for calling. How can I help you today?', 'Positive', 'None', '2023-01-01 08:00:00', '2023-01-01 08:05:09', 0, 'Happy'),
    (2, 'How may I assist you today?', 'Neutral', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:13', 0, 'Neutral'),
    (2, 'Thank you for calling. How can I help you today?', 'Negative', 'None', '2023-01-01 08:00:00', '2023-01-01 08:05:14', 0, 'Happy'),
    (2, 'How may I assist you today?', 'Positive', 'None', '2023-01-02 09:00:00', '2023-01-02 09:05:30', 0, 'Neutral');

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
