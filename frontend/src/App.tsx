import { lazy, Suspense } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';

import { AppLayout } from './components/layout/AppLayout';
import { LoadingSkeleton } from './components/common/LoadingSkeleton';

const AnalysisPage = lazy(() =>
  import('./pages/Analysis/AnalysisPage').then((module) => ({ default: module.AnalysisPage })),
);
const LandingPage = lazy(() =>
  import('./pages/Landing/LandingPage').then((module) => ({ default: module.LandingPage })),
);
const LoadingPage = lazy(() =>
  import('./pages/Loading/LoadingPage').then((module) => ({ default: module.LoadingPage })),
);
const NotFoundPage = lazy(() =>
  import('./pages/NotFound/NotFoundPage').then((module) => ({ default: module.NotFoundPage })),
);
const UploadPage = lazy(() =>
  import('./pages/Upload/UploadPage').then((module) => ({ default: module.UploadPage })),
);

export default function App() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-7xl px-5 py-10 lg:px-10"><LoadingSkeleton /></div>}>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<LandingPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/loading" element={<LoadingPage />} />
          <Route path="/analysis" element={<AnalysisPage />} />
          <Route path="/404" element={<NotFoundPage />} />
          <Route path="*" element={<Navigate to="/404" replace />} />
        </Route>
      </Routes>
    </Suspense>
  );
}
