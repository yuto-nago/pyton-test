from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from cms.models import Book
from cms.forms import BookForm
from django.views.generic.list import ListView

# Create your views here.

def book_list(request):
    """書籍の一覧"""
    #return HttpResponse('書籍の一覧')
    books = Book.objects.all().order_by('id')
    return render(request,
                  'cms/book_list.html',     # 使用するテンプレート
                  {'books': books})         # テンプレートに渡すデータ

def book_edit(request, book_id=None):
    """書籍の編集"""
    #return HttpResponse('書籍の編集')
    if book_id:  # book_id が指定されている (修正時)
        book = get_object_or_404(Book, pk=book_id)
    else:  # book_id が指定されていない (追加時)
        book = Book()

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)  # POST された request データからフォームを作成
        if form.is_valid():  # フォームのバリデーション
            book = form.save(commit=False)
            book.save()
            return redirect('cms:book_list')
    else:  # GET の時
        form = BookForm(instance=book)  # book インスタンスからフォームを作成

    return render(request, 'cms/book_edit.html', dict(form=form, book_id=book_id))

def book_del(request, book_id):
    """書籍の削除"""
    #return HttpResponse('書籍の削除')
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('cms:book_list')

class ImpressionList(ListView):
    """感想の一覧"""
    context_object_name='impressions'
    template_name='cms/impression_list.html'
    paginate_by = 2  # １ページは最大2件ずつでページングする

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['book_id'])  # 親の書籍を読む
        impressions = book.impressions.all().order_by('id')   # 書籍の子供の、感想を読む
        self.object_list = impressions

        context = self.get_context_data(object_list=self.object_list, book=book)
        return self.render_to_response(context)