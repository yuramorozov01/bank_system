import { Injectable, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IReceipt } from '../../interfaces/utils.interfaces';
import { FormGroup } from '@angular/forms';
import { ParserService } from '../utils/parser.service';
import { MaterializeService } from '../utils/materialize.service';

import { jsPDF } from 'jspdf';

@Injectable({
	providedIn: 'root',
})
export class AtmService {
	constructor(private http: HttpClient,
                private parserService: ParserService) { }

    balance(): Observable<IReceipt> {
        return this.http.get<IReceipt>('/api/v1/bank_card/balance/');
    }

    withdraw(formGroup: FormGroup): Observable<IReceipt> {
        const formData = this.parserService.getValuesFromFormGroup(formGroup);
        return this.http.put<IReceipt>(`/api/v1/bank_card/withdraw/`, formData);
    }

    printReceipt(receiptElementRef: ElementRef): void {
        const doc = new jsPDF();

        const pdfReceipt = receiptElementRef.nativeElement;

        doc.html(pdfReceipt.innerHTML, {
            callback: function (doc) {
                doc.save('receipt.pdf');
                MaterializeService.toast({'Success': 'Receipt has been successfully saved!'});
            },
            margin: [5, 5, 5, 5],
            windowWidth: 200,
            width: 150,
        });
    }
}
