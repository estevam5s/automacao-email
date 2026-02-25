'use client';

import { useEffect, useState } from 'react';
import { useAppStore } from '@/lib/store';
import { formatDateTime } from '@/lib/utils';
import { Loader2, Trash2, RefreshCw } from 'lucide-react';

export default function LogsPage() {
  const { getLogs, limparLogs, salvarLog } = useAppStore();
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filtroAcao, setFiltroAcao] = useState('Todos');
  const [filtroTabela, setFiltroTabela] = useState('Todas');

  const loadLogs = async () => {
    setLoading(true);
    try {
      let logsData = await getLogs(200);
      
      if (filtroAcao !== 'Todos') {
        logsData = logsData.filter(l => l.acao === filtroAcao);
      }
      if (filtroTabela !== 'Todas') {
        logsData = logsData.filter(l => l.tabela === filtroTabela);
      }
      
      setLogs(logsData);
    } catch (error) {
      console.error('Erro ao carregar logs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
  }, [filtroAcao, filtroTabela]);

  const handleLimpar = async () => {
    if (!confirm('Tem certeza que deseja limpar todos os logs?')) return;
    
    try {
      await limparLogs();
      await loadLogs();
    } catch (error) {
      console.error('Erro ao limpar logs:', error);
    }
  };

  const acaoIcone = (acao: string) => {
    const icons: Record<string, string> = {
      'CRIAR': '✅',
      'ATUALIZAR': '✏️',
      'DELETAR': '🗑️',
      'VISUALIZAR': '👁️',
      'ENVIAR_EMAIL': '📧',
    };
    return icons[acao] || '📋';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Logs do Sistema</h1>
          <p className="text-slate-400">Histórico de ações realizadas</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={loadLogs}
            className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-medium transition-colors"
          >
            <RefreshCw className="h-5 w-5" />
            Atualizar
          </button>
          <button
            onClick={handleLimpar}
            className="flex items-center gap-2 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg font-medium transition-colors"
          >
            <Trash2 className="h-5 w-5" />
            Limpar Logs
          </button>
        </div>
      </div>

      <div className="flex gap-4 flex-wrap">
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-1">Ação</label>
          <select
            value={filtroAcao}
            onChange={(e) => setFiltroAcao(e.target.value)}
            className="px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
          >
            <option value="Todos">Todos</option>
            <option value="CRIAR">Criar</option>
            <option value="ATUALIZAR">Atualizar</option>
            <option value="DELETAR">Deletar</option>
            <option value="VISUALIZAR">Visualizar</option>
            <option value="ENVIAR_EMAIL">Enviar E-mail</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-1">Tabela</label>
          <select
            value={filtroTabela}
            onChange={(e) => setFiltroTabela(e.target.value)}
            className="px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
          >
            <option value="Todas">Todas</option>
            <option value="funcionarios">Funcionários</option>
            <option value="funcionarios_base">Funcionários Base</option>
            <option value="configuracoes">Configurações</option>
            <option value="observacoes_gerais">Observações Gerais</option>
            <option value="logs">Logs</option>
          </select>
        </div>
      </div>

      <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
        <div className="p-4 border-b border-slate-700">
          <span className="text-slate-400">Total: </span>
          <span className="text-cyan-400 font-semibold">{logs.length} registros</span>
        </div>
        {loading ? (
          <div className="flex items-center justify-center p-8">
            <Loader2 className="h-8 w-8 animate-spin text-cyan-400" />
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-700/50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Data/Hora</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Ação</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Tabela</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Registro ID</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Usuário</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700">
                {logs.length > 0 ? (
                  logs.map((log, index) => (
                    <tr key={index} className="hover:bg-slate-700/30">
                      <td className="px-4 py-3 text-slate-400 whitespace-nowrap">
                        {log.created_at ? formatDateTime(log.created_at) : '-'}
                      </td>
                      <td className="px-4 py-3">
                        <span className="flex items-center gap-2">
                          <span>{acaoIcone(log.acao)}</span>
                          <span className="text-white">{log.acao}</span>
                        </span>
                      </td>
                      <td className="px-4 py-3 text-slate-300">{log.tabela}</td>
                      <td className="px-4 py-3 text-slate-400 font-mono text-sm">
                        {log.registro_id ? String(log.registro_id).substring(0, 20) : '-'}
                      </td>
                      <td className="px-4 py-3 text-slate-400">{log.usuario || 'sistema'}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="px-4 py-8 text-center text-slate-400">
                      Nenhum log encontrado
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
