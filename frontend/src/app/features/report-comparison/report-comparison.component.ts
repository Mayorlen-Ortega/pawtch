import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';
import { MatchComparison, Report } from '../../core/models';

@Component({
  selector: 'app-report-comparison',
  imports: [CommonModule, RouterLink],
  templateUrl: './report-comparison.component.html',
  styleUrl: './report-comparison.component.scss',
})
export class ReportComparisonComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(ApiService);
  readonly comparison = signal<MatchComparison | undefined>(undefined);
  readonly loading = signal(true);
  readonly error = signal('');

  ngOnInit(): void {
    const matchId = this.route.snapshot.paramMap.get('matchId') ?? '';
    this.api.getMatch(matchId).subscribe({
      next: (comparison) => { this.comparison.set(comparison); this.loading.set(false); },
      error: () => { this.error.set('We could not load this comparison.'); this.loading.set(false); },
    });
  }

  imageUrl(filename: string): string { return this.api.imageUrl(filename); }
  displayName(report: Report): string { return report.name || (report.type === 'lost' ? 'Lost pet report' : 'Found pet report'); }
  label(report: Report): string { return report.type === 'lost' ? 'Lost report' : 'Found report'; }
}
