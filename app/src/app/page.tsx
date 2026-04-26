import React, { useEffect, useState } from 'react';

interface NewsItem {
  title: string;
  summary: string;
  sources: string[];
  original_articles: string[];
}

export default function Home() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/news')
      .then((res) => res.json())
      .then((data) => {
        setNews(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching news:', err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl font-semibold">Cargando noticias deportivas...</div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-100 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Aggregator de Noticias Deportivas</h1>
          <p className="text-gray-600">Resúmenes inteligentes de Marca y AS</p>
        </header>

        {news.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-500">No hay noticias disponibles en este momento.</p>
          </div>
        ) : (
          <div className="grid gap-6">
            {news.map((item, index) => (
              <div key={index} className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow">
                <h2 className="text-2xl font-bold text-gray-800 mb-3">{item.title}</h2>
                <p className="text-gray-700 leading-relaxed mb-4">{item.summary}</p>
                <div className="flex flex-wrap gap-2 items-center">
                  <span className="text-sm font-medium text-gray-500 mr-2">Fuentes:</span>
                  {item.sources.map((source) => (
                    <span key={source} className="px-2 py-1 text-xs font-semibold bg-blue-100 text-blue-800 rounded uppercase">
                      {source}
                    </span>
                  ))}
                  <div className="ml-auto">
                    <a
                      href={item.original_articles[0]}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 hover:underline font-medium"
                    >
                      Leer más →
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
