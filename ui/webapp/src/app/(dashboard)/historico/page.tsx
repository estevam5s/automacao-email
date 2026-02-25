'use client';

import { useEffect, useState } from 'react';
import { useAppStore } from '@/lib/store';
import { formatCurrency, formatDate } from '@/lib/utils';
import { Loader2 } from 'lucide-react';

export default function HistoricoPage() {
  const { getHistoricoPresenca, getHistoricoPagamentos, getDataCadastramento, salvarLog } = useAppStore();
  const [activeTab, setActiveTab] = useState('presenca');
  const [presenca, setPresenca] = useState<any[]>([]);
  const [pagamentos, setPagamentos] = useState<any[]>([]);
  const [cadastramento, setCadastramento] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [busca, setBusca] = useState('');

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const [presencaData, pagamentosData, cadastramentoData] = await Promise.all([
          getHistoricoPresenca(200),
          getHistoricoPagamentos(200),
          getDataCadastramento()
        ]);
        setPresenca(presencaData);
        setPagamentos(pagamentosData);
        setCadastramento(cadastramentoData);
        
        await salvarLog({ acao: 'VISUALIZAR', tabela: 'historico', registro_id: 'historico', usuario: 'sistema' });
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const filteredPresenca = busca 
    ? presenca.filter(p => p.nome.toLowerCase().includes(busca.toLowerCase()))
    : presenca;

  const filteredPagamentos = busca
    ? pagamentos.filter(p => p.nome.toLowerCase().includes(busca.toLowerCase()))
    : pagamentos;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-cyan-400" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Histórico</h1>
        <p className="text-slate-400">Visualize o histórico completo</p>
      </div>

      <div className="flex gap-2 border-b border-slate-700 pb-4">
        {['presenca', 'pagamentos', 'cadastramento'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === tab 
                ? 'bg-cyan-500 text-white' 
                : 'bg-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            {tab === 'presenca' ? 'Presença' : tab === 'pagamentos' ? 'Pagamentos' : 'Cadastramento'}
          </button>
        ))}
      </div>

      <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
        <input
          type="text"
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
          placeholder="Buscar funcionário..."
          className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        />
      </div>

      <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-700/50">
              {activeTab === 'presenca' && (
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Data</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Funcionário</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Entrada</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Saída</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Valor</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Observação</th>
                </tr>
              )}
              {activeTab === 'pagamentos' && (
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Funcionário</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Data</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Valor</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Vale</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Tipo</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Status</th>
                </tr>
              )}
              {activeTab === 'cadastramento' && (
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Funcionário</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Primeiro Dia</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Último Dia</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Dias Trab.</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Total Recebido</th>
                </tr>
              )}
            </thead>
            <tbody className="divide-y divide-slate-700">
              {activeTab === 'presenca' && (
                filteredPresenca.length > 0 ? (
                  filteredPresenca.map((p, i) => (
                    <tr key={i} className="hover:bg-slate-700/30">
                      <td className="px-4 py-3 text-white">{p.dia_formatado || p.dia_trabalho}</td>
                      <td className="px-4 py-3 text-white">{p.nome}</td>
                      <td className="px-4 py-3 text-slate-400">{p.hora_entrada}</td>
                      <td className="px-4 py-3 text-slate-400">{p.hora_saida}</td>
                      <td className="px-4 py-3 text-cyan-400">{formatCurrency(parseFloat(String(p.valor_10_percent)) || 0)}</td>
                      <td className="px-4 py-3 text-slate-400">{p.observacao || '-'}</td>
                    </tr>
                  ))
                ) : (
                  <tr><td colSpan={6} className="px-4 py-8 text-center text-slate-400">Nenhum registro encontrado</td></tr>
                )
              )}
              {activeTab === 'pagamentos' && (
                filteredPagamentos.length > 0 ? (
                  filteredPagamentos.map((p, i) => (
                    <tr key={i} className="hover:bg-slate-700/30">
                      <td className="px-4 py-3 text-white">{p.nome}</td>
                      <td className="px-4 py-3 text-slate-400">{formatDate(p.dia_trabalho)}</td>
                      <td className="px-4 py-3 text-cyan-400">{formatCurrency(parseFloat(String(p.valor_10_percent)) || 0)}</td>
                      <td className="px-4 py-3 text-slate-400">{p.vale ? formatCurrency(parseFloat(String(p.vale))) : '-'}</td>
                      <td className="px-4 py-3 text-slate-400">{p.tipo_pagamento || '-'}</td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${p.pago ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'}`}>
                          {p.status_pagamento}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr><td colSpan={6} className="px-4 py-8 text-center text-slate-400">Nenhum registro encontrado</td></tr>
                )
              )}
              {activeTab === 'cadastramento' && (
                cadastramento.length > 0 ? (
                  cadastramento.map((c, i) => (
                    <tr key={i} className="hover:bg-slate-700/30">
                      <td className="px-4 py-3 text-white">{c.nome}</td>
                      <td className="px-4 py-3 text-slate-400">{formatDate(c.primeiro_dia_trabalho)}</td>
                      <td className="px-4 py-3 text-slate-400">{formatDate(c.ultimo_dia_trabalho)}</td>
                      <td className="px-4 py-3 text-white">{c.total_dias_trabalhados}</td>
                      <td className="px-4 py-3 text-cyan-400">{formatCurrency(c.total_recebido)}</td>
                    </tr>
                  ))
                ) : (
                  <tr><td colSpan={5} className="px-4 py-8 text-center text-slate-400">Nenhum registro encontrado</td></tr>
                )
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
