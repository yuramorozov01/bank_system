import { ElementRef } from '@angular/core';

declare var M

export class MaterializeService {
	static toast(message: string) {
		M.toast({html: message});
	}

	static initializeFloatingButton(ref: ElementRef) {
		M.FloatingActionButton.init(ref.nativeElement);
	}

	static initializeParallax(ref: ElementRef) {
		M.Parallax.init(ref.nativeElement);
	}

	static updateTextInputs() {
		M.updateTextFields();
	}
}