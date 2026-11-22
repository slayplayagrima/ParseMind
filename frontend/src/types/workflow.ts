export type WorkflowKind =
  | "resume_workflow"
  | "contract_workflow"
  | "invoice_workflow"
  | "report_workflow"
  | "policy_workflow"
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

export interface InvoiceParty {
  name: string | null;
  address: string | null;
  email: string | null;
  tax_id: string | null;
}

export interface LineItem {
  description: string;
  quantity: number | null;
  unit_price: number | null;
  amount: number | null;
}

export interface InvoiceResponse {
  invoice_number: string | null;
  issue_date: string | null;
  due_date: string | null;
  currency: string | null;
  vendor: InvoiceParty;
  customer: InvoiceParty;
  line_items: LineItem[];
  subtotal: number | null;
  tax: number | null;
  discount: number | null;
  total: number | null;
  payment_terms: string | null;
  summary: string;
  issues: string[];
}

export interface InvoiceWorkflowResult {
  invoice: InvoiceResponse;
  entities: EntityResponse;
}

export interface ReportMetric {
  name: string;
  value: string;
  context: string | null;
}

export interface ReportResponse {
  title: string | null;
  report_type: string | null;
  authors: string[];
  organization: string | null;
  publication_date: string | null;
  purpose: string | null;
  key_findings: string[];
  metrics: ReportMetric[];
  conclusions: string[];
  recommendations: string[];
  limitations: string[];
  summary: string;
}

export interface ReportWorkflowResult {
  report: ReportResponse;
  entities: EntityResponse;
}

export interface PolicyRule {
  title: string;
  description: string;
}

export interface PolicyResponse {
  title: string | null;
  policy_type: string | null;
  organization: string | null;
  effective_date: string | null;
  version: string | null;
  scope: string | null;
  applies_to: string[];
  rules: PolicyRule[];
  obligations: string[];
  prohibited: string[];
  penalties: string[];
  // Same shape as contract risks, so the risk card can show them.
  compliance_gaps: ContractRisk[];
  summary: string;
}

export interface PolicyWorkflowResult {
  policy: PolicyResponse;
  entities: EntityResponse;
}

export type WorkflowResult =
  | ContractWorkflowResult
  | ResumeWorkflowResult
  | InvoiceWorkflowResult
  | ReportWorkflowResult
  | PolicyWorkflowResult
  | Record<string, unknown>;
