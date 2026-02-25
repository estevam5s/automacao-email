'use client';

import { useEffect, useState } from 'react';
import { useAppStore } from '@/lib/store';
import { formatCurrency } from '@/lib/utils';
import { Plus, Trash2, Loader2, RefreshCw } from 'lucide-react';

export default function RegistrosPage() {
  const { getFuncionariosBase, getFuncionarios, registrarTrabalho, deletarFuncionario, getObservacaoGeral, salvarObservacaoGeral, salvarLog } = useAppStore();
  const [nomes, setNomes] = useState<string[]>([]);
  const [funcionariosDia, setFuncionariosDia] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  
  const [diaTrabalho, setDiaTrabalho] = useState(new Date().toISOString().split('T')[0]);
  const [nome, setNome] = useState('');
  const [valor10, setValor10] = useState('');
  const [horaEntrada, setHoraEntrada] = useState('08:00');
  const [horaSaida, setHoraSaida] = useState('16:00');
  const [vale, setVale] = useState('');
  const [tipoVale, setTipoVale] = useState('pix');
  const [pago, setPago] = useState(false);
  const [observacao, setObservacao] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const [nomesData, diaData, obsData] = await Promise.all([
        getFuncionariosBase(),
        getFuncionarios(diaTrabalho),
        getObservacaoGeral(diaTrabalho)
      ]);
      setNomes(nomesData.map(f => f.nome));
      setFuncionariosDia(diaData);
      setObservacao(obsData?.observacao || '');
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [diaTrabalho]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!nome || !valor10) return;

    setSaving(true);
    try {
      await registrarTrabalho({
        nome,
        dia_trabalho: diaTrabalho,
        valor_10_percent: parseFloat(valor10),
        hora_entrada: horaEntrada,
        hora_saida: horaSaida,
        vale: vale ? parseFloat(vale) : undefined,
        tipo_vale: vale ? tipoVale : undefined,
        pago,
        tipo_pagamento: 'pix',
      });
      await salvarLog({ acao: 'CRIAR', tabela: 'funcionarios', registro_id: `${nome}-${diaTrabalho}`, usuario: 'sistema' });
      
      setNome('');
      setValor10('');
      setVale('');
      setPago(false);
      loadData();
    } catch (error) {
      console.error('Erro ao registrar:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleDeletar = async (id: string) => {
    if (!confirm('Tem certeza que deseja deletar este registro?')) return;
    
    try {
      await deletarFuncionario(id);
      await salvarLog({ acao: 'DELETAR', tabela: 'funcionarios', registro_id: id, usuario: 'sistema' });
      loadData();
    } catch (error) {
      console.error('Erro ao deletar:', error);
    }
  };

  const handleSalvarObs = async () => {
    try {
      await salvarObservacaoGeral({ dia_trabalho: diaTrabalho, observacao });
      alert('Observação salva!');
    } catch (error) {
      console.error('Erro ao salvar observação:', error);
    }
  };

  const totalDia = funcionariosDia.reduce((acc, f) => acc + (parseFloat(String(f.valor_10_percent)) || 0), 0);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Registro de Trabalho</h1>
        <p className="text-slate-400">Registre o trabalho do dia</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
            <div className="flex items-center gap-4 mb-6">
              <div className="flex-1">
                <label className="block text-sm font-medium text-slate-300 mb-1">Data</label>
                <input
                  type="date"
                  value={diaTrabalho}
                  onChange={(e) => setDiaTrabalho(e.target.value)}
                  className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              </div>
              <button
                onClick={loadData}
                className="mt-6 p-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
              >
                <RefreshCw className="h-5 w-5" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Funcionário</label>
                  <select
                    value={nome}
                    onChange={(e) => setNome(e.target.value)}
                    className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                    required
                  >
                    <option value="">Selecione...</option>
                    {nomes.map(n => <option key={n} value={n}>{n}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">10% das Vendas (R$)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={valor10}
                    onChange={(e) => setValor10(e.target.value)}
                    className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                    placeholder="0.00"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Entrada</label>
                  <input
                    type="time"
                    value={horaEntrada}
                    onChange={(e) => setHoraEntrada(e.target.value)}
                    className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Saída</label>
                  <input
                    type="time"
                    value={horaSaida}
                    onChange={(e) => setHoraSaida(e.target.value)}
                    className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Vale (R$)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={vale}
                    onChange={(e) => setVale(e.target.value)}
                    className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                    placeholder="0.00"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Tipo do Vale</label>
                  <select
                    value={tipoVale}
                    onChange={(e) => setTipoVale(e.target.value)}
                    className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  >
                    <option value="pix">PIX</option>
                    <option value="dinheiro">Dinheiro</option>
                  </select>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={pago}
                    onChange={(e) => setPago(e.target.checked)}
                    className="w-5 h-5 rounded bg-slate-900 border-slate-600 text-cyan-500 focus:ring-cyan-500"
                  />
                  <span className="text-white">Salário Pago</span>
                </label>
              </div>

              <button
                type="submit"
                disabled={saving}
                className="flex items-center gap-2 px-6 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
              >
                {saving ? <Loader2 className="h-5 w-5 animate-spin" /> : <Plus className="h-5 w-5" />}
                Adicionar Registro
              </button>
            </form>
          </div>

          <div className="bg-slate-800 rounded-xl border border-slate-700">
            <div className="p-4 border-b border-slate-700 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-white">Registros do Dia</h2>
              <span className="text-cyan-400 font-semibold">Total: {formatCurrency(totalDia)}</span>
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
                      <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Nome</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">10%</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Entrada</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Saída</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Vale</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Pago</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-slate-400 uppercase">Ações</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-700">
                    {funcionariosDia.length > 0 ? (
                      funcionariosDia.map((func) => (
                        <tr key={func.id} className="hover:bg-slate-700/30">
                          <td className="px-4 py-3 text-white">{func.nome}</td>
                          <td className="px-4 py-3 text-cyan-400">{formatCurrency(parseFloat(String(func.valor_10_percent)) || 0)}</td>
                          <td className="px-4 py-3 text-slate-400">{func.hora_entrada}</td>
                          <td className="px-4 py-3 text-slate-400">{func.hora_saida}</td>
                          <td className="px-4 py-3 text-slate-400">{func.vale ? formatCurrency(parseFloat(String(func.vale))) : '-'}</td>
                          <td className="px-4 py-3">
                            <span className={`px-2 py-1 rounded text-xs font-medium ${func.pago ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'}`}>
                              {func.pago ? 'Pago' : 'Pendente'}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <button
                              onClick={() => handleDeletar(func.id)}
                              className="p-1 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded transition-colors"
                            >
                              <Trash2 className="h-4 w-4" />
                            </button>
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={7} className="px-4 py-8 text-center text-slate-400">
                          Nenhum registro para esta data
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Observação do Dia</h2>
            <textarea
              value={observacao}
              onChange={(e) => setObservacao(e.target.value)}
              className="w-full h-32 px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500 resize-none"
              placeholder="Observações sobre o dia..."
            />
            <button
              onClick={handleSalvarObs}
              className="mt-4 w-full flex items-center justify-center gap-2 px-4 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg font-medium transition-colors"
            >
              Salvar Observação
            </button>
          </div>

          <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Resumo do Dia</h2>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-400">Total Funcionários:</span>
                <span className="text-white font-medium">{funcionariosDia.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Total 10%:</span>
                <span className="text-cyan-400 font-medium">{formatCurrency(totalDia)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Pagos:</span>
                <span className="text-green-400 font-medium">
                  {funcionariosDia.filter(f => f.pago).length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Pendentes:</span>
                <span className="text-yellow-400 font-medium">
                  {funcionariosDia.filter(f => !f.pago).length}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
