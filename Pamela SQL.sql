-- Creating the Company table
CREATE TABLE Company (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(60)
);



-- Creating the Agent table
CREATE TABLE Agent (
    Id SERIAL PRIMARY KEY,
    RegistrationDate DATE,
    Username VARCHAR(60),
    CompanyId INT,
    FOREIGN KEY (CompanyId) REFERENCES Company(Id)
);



-- Creating the Call table
CREATE TABLE Call (
    Id SERIAL PRIMARY KEY,
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    AgentId INT,
    CallScore SMALLINT,
    Duration INT,
    FOREIGN KEY (AgentId) REFERENCES Agent(Id)
);


-- Creating the CallInfo table
CREATE TABLE CallInfo (
    CallId INT PRIMARY KEY,
    Topic VARCHAR(60),
    ClientInterrupts INT,
    AgentInterrupts INT,
    SilencePercent SMALLINT,
    ClientSpeechDuration INT,
    AgentSpeechDuration INT,
    client_hatespeechpercent SMALLINT,
    agent_hatespeechpercent SMALLINT,
    client_ironypercent SMALLINT,
    agent_ironypercent SMALLINT,
    customer_satisfaction_rate SMALLINT,
    agent_performance_rate SMALLINT,
    alert boolean,
    FOREIGN KEY (CallId) REFERENCES Call(Id)
);
--satisfactiony poxel
--alert boolean



-- Creating the Call_Mood_Agent table
CREATE TABLE Call_Mood_Agent (
    CallId INT,
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    Emotion VARCHAR(10),
    PRIMARY KEY (CallId, StartTime, EndTime),
    FOREIGN KEY (CallId) REFERENCES Call(Id)
);
--emotion_in_number INT, change 

-- Creating the Call_Mood_Client table
CREATE TABLE Call_Mood_Client (
    CallId INT,
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    Emotion VARCHAR(10),
    PRIMARY KEY (CallId, StartTime, EndTime),
    FOREIGN KEY (CallId) REFERENCES Call(Id)
);
--emotion_in_number INT, change

-- Creating the Call_Sentence_Agent table
CREATE TABLE Call_Sentence_Agent (
    Id SERIAL PRIMARY KEY,
    CallId INT,
    SpeechText VARCHAR(200),
    Sentiment VARCHAR(40),
    Irony VARCHAR(40),
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    HateLevelPercent SMALLINT,
    MeanEmotion VARCHAR(10),
    FOREIGN KEY (CallId) REFERENCES Call(Id)
);



-- Creating the Call_Sentence_Client table
CREATE TABLE Call_Sentence_Client (
    Id SERIAL PRIMARY KEY,
    CallId INT,
    SpeechText VARCHAR(200),
    Sentiment VARCHAR(40),
    Irony VARCHAR(40),
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    HateLevelPercent SMALLINT,
    MeanEmotion VARCHAR(10),
    FOREIGN KEY (CallId) REFERENCES Call(Id)
);



-- Creating the Call_Sentence_Aspect_Agent table
CREATE TABLE Call_Sentence_Aspect_Agent (
    Id SERIAL PRIMARY KEY,
    CallSentenceId INT,
    Aspect VARCHAR(40),
    Sentiment VARCHAR(40),
    Opinion VARCHAR(40),
    FOREIGN KEY (CallSentenceId) REFERENCES Call_Sentence_Agent(Id)
);



-- Creating the Call_Sentence_Aspect_Client table
CREATE TABLE Call_Sentence_Aspect_Client (
    Id SERIAL PRIMARY KEY,
    CallSentenceId INT,
    Aspect VARCHAR(40),
    Sentiment VARCHAR(40),
    Opinion VARCHAR(40),
    FOREIGN KEY (CallSentenceId) REFERENCES Call_Sentence_Client(Id)
);