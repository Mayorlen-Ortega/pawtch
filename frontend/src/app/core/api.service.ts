import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { LocationOption, Match, MatchComparison, Report } from './models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = 'http://localhost:8000/api';

  getLocations(): Observable<LocationOption[]> {
    return this.http.get<LocationOption[]>(`${this.baseUrl}/locations`);
  }

  createReport(payload: Record<string, string>, photo: File): Observable<Report> {
    const formData = new FormData();
    formData.append('report', JSON.stringify(payload));
    formData.append('photo', photo);
    return this.http.post<Report>(`${this.baseUrl}/reports`, formData);
  }

  getReport(id: string): Observable<Report> {
    return this.http.get<Report>(`${this.baseUrl}/reports/${id}`);
  }

  getMatches(id: string): Observable<Match[]> {
    return this.http.get<Match[]>(`${this.baseUrl}/reports/${id}/matches`);
  }

  getMatch(id: string): Observable<MatchComparison> {
    return this.http.get<MatchComparison>(`${this.baseUrl}/matches/${id}`);
  }

  imageUrl(filename: string): string {
    return `http://localhost:8000/media/${filename}`;
  }
}
