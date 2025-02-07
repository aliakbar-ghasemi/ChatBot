export class StreamService {
  private abortController: AbortController | null = null
  private decoder = new TextDecoder()
  
  async* streamResponse(response: Response) {
    this.abortController = new AbortController()
    const reader = response.body?.getReader()
    
    try {
      while (true) {
        if (this.abortController.signal.aborted) {
          reader?.cancel()
          break
        }
        
        const { done, value } = await reader?.read() || {}
        if (done) break
        yield this.decoder.decode(value)
      }
    } finally {
      reader?.cancel()
    }
  }

  cancelStream() {
    this.abortController?.abort()
  }
}
