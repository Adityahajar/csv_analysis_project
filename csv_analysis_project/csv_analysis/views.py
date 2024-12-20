import pandas as pd
from django.shortcuts import render, redirect
from .forms import CSVFileForm
from .models import CSVFile
import matplotlib.pyplot as plt
import seaborn as sns
import os

def upload_file(request):
    if request.method == 'POST':
        form = CSVFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.save()
            return redirect('analyze_file', file_id=csv_file.id)
    else:
        form = CSVFileForm()
    return render(request, 'csv_analysis/templates/upload.html', {'form': form})

def analyze_file(request, file_id):
    csv_file = CSVFile.objects.get(id=file_id)
    df = pd.read_csv(csv_file.file.path)

    # Perform data analysis
    head = df.head()
    description = df.describe()
    missing_values = df.isnull().sum()

    # Generate plots
    plt.figure(figsize=(10, 6))
    sns.histplot(df.select_dtypes(include=['float64', 'int64']).iloc[:, 0], kde=True)
    plot_path = os.path.join('media', 'plots', f'{csv_file.id}_plot.png')
    if not os.path.exists('media/plots'):
        os.makedirs('media/plots')
    plt.savefig(plot_path)
    plt.close()

    context = {
        'head': head.to_html(),
        'description': description.to_html(),
        'missing_values': missing_values.to_dict(),
        'plot_path': plot_path,
    }
    #print(context,"this is context")
    return render(request, 'csv_analysis/templates/analyze.html', context)
