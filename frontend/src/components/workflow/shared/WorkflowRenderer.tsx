import type { WorkflowResponse } from '../../../types/workflow';
import { titleCase } from '../../../utils/format';
import { hasContractResult, hasResumeResult } from '../../../utils/typeGuards';
import { EmptyState } from '../../common/EmptyState';
import { ContractRenderer } from '../contract/ContractRenderer';
import { ResumeRenderer } from '../resume/ResumeRenderer';

interface WorkflowRendererProps {
  response: WorkflowResponse;
}

export const WorkflowRenderer = ({ response }: WorkflowRendererProps) => {
  const workflow = response.metadata.workflow.toLowerCase();

  if (workflow === "contract_workflow" && hasContractResult(response)) {
    return <ContractRenderer result={response.result} />;
  }

  if (workflow === "resume_workflow" && hasResumeResult(response)) {
    return <ResumeRenderer result={response.result} />;
  }

  return (
    <EmptyState
      title={`${titleCase(response.metadata.workflow)} renderer unavailable`}
      description="This workflow was detected by the backend, but no frontend renderer has been registered for it yet."
    />
  );
};