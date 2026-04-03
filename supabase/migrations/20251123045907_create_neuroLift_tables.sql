/*
  # NeuroLift Technologies Simulation Environment - Database Schema

  1. New Tables
    - `avatars` - AI Avatar instances with ADHD traits
    - `avatar_progress` - Learning progress tracking for each Avatar
    - `aides` - AI Aide coaching instances
    - `training_sessions` - Individual training session records
    - `task_results` - Results of Avatar task attempts
    - `coaching_actions` - Coaching interventions provided by Aides
    - `burnout_assessments` - Burnout risk evaluations
    - `metrics` - Aggregated performance metrics

  2. Security
    - Enable RLS on all tables
    - Implement appropriate access policies
    - Ensure data isolation between training sessions

  3. Key Features
    - Comprehensive tracking of Avatar learning journey
    - Full audit trail of coaching interventions
    - Performance metrics and progress indicators
    - Burnout risk monitoring
*/

-- Create avatars table
CREATE TABLE IF NOT EXISTS avatars (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  avatar_id text UNIQUE NOT NULL,
  trait_name text NOT NULL,
  trait_config jsonb NOT NULL,
  current_state text DEFAULT 'idle',
  emotional_state text DEFAULT 'neutral',
  cognitive_load float DEFAULT 0.0,
  stress_level float DEFAULT 0.0,
  burnout_risk_level float DEFAULT 0.0,
  total_tasks_attempted integer DEFAULT 0,
  total_tasks_completed integer DEFAULT 0,
  total_coaching_sessions integer DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  last_activity timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create avatar_progress table
CREATE TABLE IF NOT EXISTS avatar_progress (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  avatar_id uuid NOT NULL REFERENCES avatars(id) ON DELETE CASCADE,
  task_type text NOT NULL,
  attempts integer DEFAULT 0,
  successes integer DEFAULT 0,
  success_rate float DEFAULT 0.0,
  independence_level float DEFAULT 0.0,
  coaching_sessions integer DEFAULT 0,
  last_improved_at timestamptz,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(avatar_id, task_type)
);

-- Create aides table
CREATE TABLE IF NOT EXISTS aides (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  aide_id text UNIQUE NOT NULL,
  expertise_area text NOT NULL,
  expertise_config jsonb NOT NULL,
  total_interventions integer DEFAULT 0,
  successful_interventions integer DEFAULT 0,
  crisis_interventions integer DEFAULT 0,
  independence_achievements integer DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  last_intervention timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create training_sessions table
CREATE TABLE IF NOT EXISTS training_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id text UNIQUE NOT NULL,
  avatar_id uuid NOT NULL REFERENCES avatars(id) ON DELETE CASCADE,
  aide_id uuid NOT NULL REFERENCES aides(id) ON DELETE CASCADE,
  session_type text NOT NULL,
  status text DEFAULT 'in_progress',
  scenario text,
  start_time timestamptz DEFAULT now(),
  end_time timestamptz,
  duration_seconds integer,
  session_data jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create task_results table
CREATE TABLE IF NOT EXISTS task_results (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  training_session_id uuid NOT NULL REFERENCES training_sessions(id) ON DELETE CASCADE,
  avatar_id uuid NOT NULL REFERENCES avatars(id) ON DELETE CASCADE,
  task_type text NOT NULL,
  success boolean NOT NULL,
  completion_time_seconds float,
  quality_score float DEFAULT 0.0,
  struggle_indicators text[] DEFAULT '{}',
  emotional_state text,
  cognitive_load float DEFAULT 0.0,
  result_data jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

-- Create coaching_actions table
CREATE TABLE IF NOT EXISTS coaching_actions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  coaching_id text UNIQUE NOT NULL,
  training_session_id uuid NOT NULL REFERENCES training_sessions(id) ON DELETE CASCADE,
  avatar_id uuid NOT NULL REFERENCES avatars(id) ON DELETE CASCADE,
  aide_id uuid NOT NULL REFERENCES aides(id) ON DELETE CASCADE,
  coaching_type text NOT NULL,
  urgency text NOT NULL,
  strategy text NOT NULL,
  techniques text[] DEFAULT '{}',
  expected_outcomes text[] DEFAULT '{}',
  stress_reduction float DEFAULT 0.0,
  emotional_boost float DEFAULT 0.0,
  cognitive_support float DEFAULT 0.0,
  independence_building float DEFAULT 0.0,
  action_data jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

-- Create burnout_assessments table
CREATE TABLE IF NOT EXISTS burnout_assessments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  avatar_id uuid NOT NULL REFERENCES avatars(id) ON DELETE CASCADE,
  aide_id uuid NOT NULL REFERENCES aides(id) ON DELETE CASCADE,
  risk_level text NOT NULL,
  risk_score float NOT NULL,
  contributing_factors text[] DEFAULT '{}',
  early_warning_signs text[] DEFAULT '{}',
  intervention_recommendations text[] DEFAULT '{}',
  rrt_activation_needed boolean DEFAULT false,
  assessment_data jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

-- Create metrics table for aggregated data
CREATE TABLE IF NOT EXISTS metrics (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  avatar_id uuid REFERENCES avatars(id) ON DELETE CASCADE,
  aide_id uuid REFERENCES aides(id) ON DELETE CASCADE,
  metric_type text NOT NULL,
  metric_value float NOT NULL,
  metric_data jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE avatars ENABLE ROW LEVEL SECURITY;
ALTER TABLE avatar_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE aides ENABLE ROW LEVEL SECURITY;
ALTER TABLE training_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE task_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE coaching_actions ENABLE ROW LEVEL SECURITY;
ALTER TABLE burnout_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE metrics ENABLE ROW LEVEL SECURITY;

-- RLS Policies - Allow all authenticated users to access (for development)
-- In production, implement stricter policies based on user roles

CREATE POLICY "Avatars readable by authenticated users"
  ON avatars FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Avatars writable by authenticated users"
  ON avatars FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Avatars updatable by authenticated users"
  ON avatars FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Avatar progress readable by authenticated users"
  ON avatar_progress FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Avatar progress writable by authenticated users"
  ON avatar_progress FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Avatar progress updatable by authenticated users"
  ON avatar_progress FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Aides readable by authenticated users"
  ON aides FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Aides writable by authenticated users"
  ON aides FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Aides updatable by authenticated users"
  ON aides FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Training sessions readable by authenticated users"
  ON training_sessions FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Training sessions writable by authenticated users"
  ON training_sessions FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Training sessions updatable by authenticated users"
  ON training_sessions FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Task results readable by authenticated users"
  ON task_results FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Task results writable by authenticated users"
  ON task_results FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Coaching actions readable by authenticated users"
  ON coaching_actions FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Coaching actions writable by authenticated users"
  ON coaching_actions FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Burnout assessments readable by authenticated users"
  ON burnout_assessments FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Burnout assessments writable by authenticated users"
  ON burnout_assessments FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Metrics readable by authenticated users"
  ON metrics FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Metrics writable by authenticated users"
  ON metrics FOR INSERT
  TO authenticated
  WITH CHECK (true);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_avatars_avatar_id ON avatars(avatar_id);
CREATE INDEX IF NOT EXISTS idx_avatars_trait_name ON avatars(trait_name);
CREATE INDEX IF NOT EXISTS idx_avatars_created_at ON avatars(created_at);
CREATE INDEX IF NOT EXISTS idx_avatar_progress_avatar_id ON avatar_progress(avatar_id);
CREATE INDEX IF NOT EXISTS idx_avatar_progress_task_type ON avatar_progress(task_type);
CREATE INDEX IF NOT EXISTS idx_aides_aide_id ON aides(aide_id);
CREATE INDEX IF NOT EXISTS idx_aides_expertise_area ON aides(expertise_area);
CREATE INDEX IF NOT EXISTS idx_training_sessions_avatar_id ON training_sessions(avatar_id);
CREATE INDEX IF NOT EXISTS idx_training_sessions_aide_id ON training_sessions(aide_id);
CREATE INDEX IF NOT EXISTS idx_training_sessions_status ON training_sessions(status);
CREATE INDEX IF NOT EXISTS idx_task_results_avatar_id ON task_results(avatar_id);
CREATE INDEX IF NOT EXISTS idx_task_results_session_id ON task_results(training_session_id);
CREATE INDEX IF NOT EXISTS idx_coaching_actions_avatar_id ON coaching_actions(avatar_id);
CREATE INDEX IF NOT EXISTS idx_coaching_actions_aide_id ON coaching_actions(aide_id);
CREATE INDEX IF NOT EXISTS idx_burnout_assessments_avatar_id ON burnout_assessments(avatar_id);
CREATE INDEX IF NOT EXISTS idx_metrics_avatar_id ON metrics(avatar_id);
CREATE INDEX IF NOT EXISTS idx_metrics_metric_type ON metrics(metric_type);
