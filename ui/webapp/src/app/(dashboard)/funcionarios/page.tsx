'use client';

import { useEffect, useState } from 'react';
import { useAppStore } from '@/lib/store';
import { formatDate } from '@/lib/utils';
import { Plus, Trash2, User, Loader2 } from 'lucide-react';

export default function FuncionariosPage() {
  const { getFuncionariosBase, cadastrarFuncionarioBase, deletarFuncionarioBase, salvarLog } = useAppStore();
  const [funcionarios, setFuncionarios] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [newNome, setNewNome] = useState('');
  const [newPix, setNewPix] = useState('');
  const [saving, setSaving] = useState(false);

  const loadFuncionarios = async () => {
    try {
      const data = await getFuncionariosBase();
      setFuncionarios(data);
    } catch (error) {
      console.error('Erro ao carregar funcionários:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFuncionarios();
  }, []);

  const handleCadastrar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newNome.trim()) return;
    
    setSaving(true);
    try {
      await cadastrarFuncionarioBase({ nome: newNome, pix: newPix || undefined });
      await salvarLog({ acao: 'CRIAR', tabela: 'funcionarios_base', registro_id: newNome, usuario: 'sistema' });
      setNewNome('');
      setNewPix('');
      setShowForm(false);
      loadFuncionarios();
    } catch (error) {
      console.error('Erro ao cadastrar:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleDeletar = async (id: string, nome: string) => {
    if (!confirm('Tem certeza que deseja deletar este funcionário?')) return;
    
    try {
      await deletarFuncionarioBase(id);
      await salvarLog({ acao: 'DELETAR', tabela: 'funcionarios_base', registro_id: id, usuario: 'sistema' });
      loadFuncionarios();
    } catch (error) {
      console.error('Erro ao deletar:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-cyan-400" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Funcionários</h1>
          <p className="text-slate-400">Gerencie a lista de funcionários</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 px-4 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg font-medium transition-colors"
        >
          <Plus className="h-5 w-5" />
          Novo Funcionário
        </button>
      </div>

      {showForm && (
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
          <h2 className="text-lg font-semibold text-white mb-4">Cadastrar Novo Funcionário</h2>
          <form onSubmit={handleCadastrar} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Nome</label>
                <input
                  type="text"
                  value={newNome}
                  onChange={(e) => setNewNome(e.target.value)}
                  className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  placeholder="Nome do funcionário"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">PIX (opcional)</label>
                <input
                  type="text"
                  value={newPix}
                  onChange={(e) => setNewPix(e.target.value)}
                  className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  placeholder="Chave PIX"
                />
              </div>
            </div>
            <div className="flex gap-3">
              <button
                type="submit"
                disabled={saving}
                className="flex items-center gap-2 px-4 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
              >
                {saving ? <Loader2 className="h-5 w-5 animate-spin" /> : <Plus className="h-5 w-5" />}
                Cadastrar
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-medium transition-colors"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-700/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Nome</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">PIX</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Data Cadastro</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700">
            {funcionarios.length > 0 ? (
              funcionarios.map((func) => (
                <tr key={func.id} className="hover:bg-slate-700/30">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-cyan-500/20 rounded-full flex items-center justify-center">
                        <User className="h-4 w-4 text-cyan-400" />
                      </div>
                      <span className="text-white font-medium">{func.nome}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-slate-400">{func.pix || '-'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-slate-400">{func.created_at ? formatDate(func.created_at) : '-'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <button
                      onClick={() => handleDeletar(func.id, func.nome)}
                      className="p-2 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-lg transition-colors"
                    >
                      <Trash2 className="h-5 w-5" />
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={4} className="px-6 py-8 text-center text-slate-400">
                  Nenhum funcionário cadastrado
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
