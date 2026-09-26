export type ReportType = 'lost' | 'found';

export interface LocationOption {
  id: string;
  name: string;
}

export interface Report {
  id: string;
  type: ReportType;
  photo: string;
  species: string;
  color: string;
  markings: string;
  name?: string;
  sex?: string;
  size?: string;
  description?: string;
  locationId: string;
  locationName: string;
  date: string;
  createdAt: string;
}

export interface Match {
  id: string;
  lostReportId: string;
  foundReportId: string;
  visualScore: number;
  physicalScore: number;
  geographicScore: number;
  dateScore: number;
  weightedIndication: number;
  isPossibleMatch: boolean;
  explanations: string[];
  otherReport: Report;
}

export interface MatchComparison extends Omit<Match, 'otherReport'> {
  lostReport: Report;
  foundReport: Report;
}
