import { ElementRef } from '@angular/core';

declare var M

export class MaterializeService {
	static toast(msg: any) {
        Object.keys(msg).forEach((key) => {
            M.toast({html: key + ': ' + msg[key]});
        });
	}

	static initializeFloatingButton(ref: ElementRef) {
		M.FloatingActionButton.init(ref.nativeElement);
	}

	static initializeParallax(ref: ElementRef) {
		M.Parallax.init(ref.nativeElement);
	}
    static initializeSelect(ref: ElementRef) {
        M.FormSelect.init(ref.nativeElement);
    }

	static updateTextInputs() {
		M.updateTextFields();
	}
}
