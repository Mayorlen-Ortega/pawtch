import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';
import { Match, Report } from '../../core/models';

@Component({ selector: 'app-report-detail', imports: [CommonModule, RouterLink], templateUrl: './report-detail.component.html', styleUrl: './report-detail.component.scss' })
export class ReportDetailComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(ApiService);
  readonly report = signal<Report | undefined>(undefined);
  readonly matches = signal<Match[]>([]);
  readonly created = signal(false);
  readonly loading = signal(true);
  readonly error = signal('');
  ngOnInit(): void { const id = this.route.snapshot.paramMap.get('id') ?? ''; this.created.set(this.route.snapshot.queryParamMap.get('created') === '1'); this.api.getReport(id).subscribe({ next: (report) => { this.report.set(report); this.loading.set(false); }, error: () => { this.error.set('We could not find that report.'); this.loading.set(false); } }); this.api.getMatches(id).subscribe({ next: (matches) => this.matches.set(matches) }); }
  imageUrl(filename: string): string { return this.api.imageUrl(filename); }
}
