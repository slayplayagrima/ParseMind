export type WorkflowKind =
  | "resume_workflow"
  | "contract_workflow"
  | string;

export interface WorkflowMetadata {
  workflow: WorkflowKind;
  success: boolean;
  model: string;
  confidence: number;
  execution_time_ms: number;
}

export interface WorkflowResponse<TResult = WorkflowResult> {
  metadata: WorkflowMetadata;
  result: TResult;
}

export interface APIResponse<T> {
  success: boolean;
  data: T | null;
  error: string | null;
}

export interface AnalysisEnvelope {
  fileName: string;
  analyzedAt: string;
  response: WorkflowResponse;
}

export interface EntityResponse {
  people: string[];
  organizations: string[];
  emails: string[];
  phones: string[];
  locations: string[];
  dates: string[];
  money: string[];
  skills: string[];
  technologies: string[];
}

export interface Party {
  name: string;
  role: string;
}

export interface PaymentTerms {
  amount: string | null;
  currency: string | null;
  due_date: string | null;
  frequency: string | null;
}

export interface Clause {
  title: string;
  description: string;
}

export type RiskSeverity = 'low' | 'medium' | 'high' | 'critical';

export interface ContractRisk {
  title: string;
  severity: RiskSeverity;
  explanation: string;
  recommendation: string;
}

export interface ContractResponse {
  contract_type: string;
  title: string;
  summary: string;
  parties: Party[];
  effective_date: string | null;
  termination_date: string | null;
  duration: string | null;
  governing_law: string | null;
  jurisdiction: string | null;
  payment_terms: PaymentTerms | null;
  obligations: string[];
  important_clauses: Clause[];
  risks: ContractRisk[];
  recommendations: string[];
}

export interface ContractWorkflowResult {
  contract: ContractResponse;
  entities: EntityResponse;
}

export interface Candidate {
  name: string;
  email: string;
  phone: string;
  location: string;
}

export interface Education {
  degree: string;
  institution: string;
  start_year: number | null;
  end_year: number | null;
}

export interface Experience {
  company: string;
  role: string;
  duration: string;
  description: string;
}

export interface Project {
  name: string;
  description: string;
}

export interface ResumeResponse {
  candidate: Candidate;
  summary: string;
  education: Education[];
  experience: Experience[];
  projects: Project[];
  skills: string[];
  certifications: string[];
  strengths: string[];
  improvements: string[];
  ats_score?: number;
}

export interface ResumeWorkflowResult {
  resume: ResumeResponse;
  entities: EntityResponse;
}

export type WorkflowResult = ContractWorkflowResult | ResumeWorkflowResult | Record<string, unknown>;
