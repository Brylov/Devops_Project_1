import { Component, Injector } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TranslationService } from '../services/translation.service';


@Component({
  selector: 'app-main',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './main.component.html',
  styleUrl: './main.component.scss'
})
export class MainComponent {
  inputText: string = '';
  translatedText: string = '';

  constructor(private translationService: TranslationService) {}


  translateText(): void {
    this.translationService.translateText(this.inputText).subscribe(
      (response) => {
        console.log(this.inputText)
        this.translatedText = response.translated_text;
      },
      (error) => {
        console.error('Error:', error);
      }
    );
  }
  
}
